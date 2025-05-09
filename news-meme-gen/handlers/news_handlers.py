import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message, CallbackQuery, ReplyKeyboardMarkup, \
    ReplyKeyboardRemove, KeyboardButton
from aiogram.types.input_file import FSInputFile
from config.config import model, bot
from keyboards.keyboards import rating_keyboard
from lexicon.lexicon import LEXICON_RU
from config.config import model, database
from uuid import uuid1
from states.states import Joke
from censorship import must_be_censored
from states.states import MemeMaking
import logging

logger = logging.getLogger(__name__)
rt = Router()
lexicon = LEXICON_RU

N_JOKES = 3

@rt.message(Command('censor'))
async def switch_censorship(msg: Message):
    current = database['users'][str(msg.from_user.id)]['censorship_on']
    database['users'][str(msg.from_user.id)]['censorship_on'] = not current
    database.write()
    await msg.answer(lexicon['censorship_on' if not current is True else 'censorship_off'])


async def voice_gen(msg: Message, censor=True):
    dest = f"temp/{uuid1()}"
    await bot.download(msg.voice, destination=dest) # type: ignore[arg-type]
    gen = model.audio(dest)
    os.remove(dest)
    if censor and must_be_censored(gen):
        return lexicon["censored"] % gen
    return lexicon["model_answer"] % gen
    

async def text_gen(msg: str, censor=False,block_on_censor=False):
    gen = model.text(msg)
    if censor and must_be_censored(gen):
        if block_on_censor:
            return lexicon['blocked']
        else:
            return lexicon["censored"] % gen
    return lexicon["model_answer"] % gen
    

@rt.callback_query(F.data.startswith("rating_"), StateFilter(Joke.rating))
async def save_rating(clb: CallbackQuery, state: FSMContext):
    rating = int(clb.data.replace('rating_', ''))
    data = await state.get_data()
    database['jokes'].append(
        {
            "joke": data["joke_to_rate_or_memepic_path"],
            "topic": data["topic_for_joke_to_rate"],
            "rating": rating
        }
        )
    database.write()
    await clb.message.answer(lexicon["rating_ended"])
    await state.clear()


async def rate(msg: Message, state: FSMContext, topic: str, joke: str | None = None, memepic_path : str | None = None):
    assert (memepic_path is not None) ^ (joke is not None), "Pass either joke or memepic path"
    await state.set_state(Joke.rating)
    if joke:
        await msg.answer(
            lexicon["rate_joke"],
            reply_markup=rating_keyboard
            )
    if memepic_path:
        await msg.answer(
            lexicon["rate_joke"],
            reply_markup=rating_keyboard
            )
    await state.set_data((await state.get_data()) | {"joke_to_rate_or_memepic_path": joke, "topic_for_joke_to_rate": topic})


async def make_joke(msg: Message,  state: FSMContext, censor=True, block_on_censor=False):
    if msg.video:
        text = msg.caption
    else:
        text = msg.text
    if text:
        joke = await text_gen(msg.text, censor,block_on_censor=block_on_censor)
        await msg.answer(joke)
        logger.info(f"""
Generated joke from user: {msg.from_user.id}
For prompt:
{msg.text}
Censorship: {censor}
Blocking: {block_on_censor}
Result:
{joke}
""")
        return joke

    if msg.photo:
        photo = msg.photo[-1] # type: ignore[index] # Get the highest resolution photo
        user_img = f"temp/{uuid1()}.jpg"
        await bot.download(photo.file_id, destination=user_img)
        # photo_path = await photo_gen(msg)
        if not msg.caption:
            btns = [[KeyboardButton(text=str(i))] for i in range(1,3+1)]
            markup = ReplyKeyboardMarkup(
                keyboard=btns,
                one_time_keyboard=True
                )
            await msg.answer(lexicon['select_meme_style'], reply_markup=markup)
            await state.set_state(MemeMaking.waiting_for_style)
            await state.set_data(
                (await state.get_data()) | {'user_img': user_img}
                )
        else:
            joke = await text_gen(msg.caption, censor)
            logger.info(f"""
Generated joke from user: {msg.from_user.id}
For prompt:
{msg.text}
Censorship: {censor}
Blocking: {block_on_censor}
Result:
{joke}
""")
            model.image_model.template_n = 3
            path = f"temp/{uuid1()}.jpg"
            model.image(user_img, path)
            await msg.answer_photo(FSInputFile(path), caption=joke)
            
    if msg.voice:
        joke = await voice_gen(msg)
        await msg.answer(joke)
        return joke
        

@rt.message(StateFilter(MemeMaking.waiting_for_style), F.text.in_('123'))
async def select_style(msg: Message, state: FSMContext):
    style = int(msg.text)
    user_img = (await state.get_data())['user_img']
    path = f"temp/{uuid1()}.jpg"
    model.image_model.template_n = style
    model.image(user_img, path)
    await msg.answer_photo(FSInputFile(path))
    await state.clear()

@rt.message(StateFilter(default_state))
async def news_handler(msg: Message, state: FSMContext, do_rate=False):
    censor = database['users'][str(msg.from_user.id)]
    await msg.answer(lexicon["text_preloader"])
    result = await make_joke(msg=msg, state=state, censor=True, block_on_censor=True)
    if (msg.text or msg.voice) and do_rate:
        await rate(msg, topic=msg.text, joke=result, state=state, censor=censor)

@rt.message()
async def else_handler(msg: Message):
    await msg.answer(lexicon["else_handler"])