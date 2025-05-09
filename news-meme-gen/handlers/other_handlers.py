import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


from aiogram import Router
from aiogram.filters import StateFilter, CommandStart, Command
from filters.filters import AdminFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from keyboards.keyboards import rating_keyboard
from lexicon.lexicon import LEXICON_RU
from config.config import ADMIN_IDS, database


rt = Router()
lexicon = LEXICON_RU


@rt.message(CommandStart())
async def start(msg: Message, state: FSMContext):
    await state.clear()
    await msg.answer(lexicon["start"])


@rt.message(Command("help_admin"), AdminFilter(ADMIN_IDS))
async def help_admin(msg: Message):
    await msg.answer(lexicon["help_admin"])

@rt.message(Command('auth'))
async def auth(msg: Message):
    database['users'][str(msg.from_user.id)]['password'] = msg.text.replace('/auth','').strip()
    database.write()
    await msg.answer(lexicon['password_set'])