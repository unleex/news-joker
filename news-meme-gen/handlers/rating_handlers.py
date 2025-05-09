import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))


from aiogram import Router, F
from aiogram.filters import Command, StateFilter
from filters.filters import AdminFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state
from aiogram.types import Message
from config.config import model, bot, ADMIN_IDS, rated_jokes
from keyboards.keyboards import rating_keyboard
from lexicon.lexicon import LEXICON_RU, joke_added
from uuid import uuid1
from states.states import RatingJoke
import pandas as pd
import os
import random

rt = Router()
lexicon = LEXICON_RU
import sqlite3
import os
import pandas as pd

db_path = 'db/ratings.db'
all_jokes_path = 'data/jokes_to_rate.csv'

# Ensure DB directory exists
os.makedirs(os.path.dirname(db_path), exist_ok=True)

# Initialize the SQLite ratings table if not exists
def init_ratings_db():
    with sqlite3.connect(db_path) as conn:
        conn.execute("""
            CREATE TABLE IF NOT EXISTS ratings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                joke TEXT,
                user TEXT,
                topic TEXT,
                rating INTEGER
            )
        """)

# Call initialization
init_ratings_db()

# Load all_jokes as before (if still coming from CSV)
all_jokes = pd.read_csv(all_jokes_path)
def get_joke(user_id: int | str):
    user_id = str(user_id)
    if user_id not in rated_jokes: 
        rated_jokes[user_id] = []
        unrated_jokes = all_jokes
    else:
        unrated_jokes = all_jokes[~all_jokes['joke'].isin(rated_jokes[user_id])]
    if not unrated_jokes.empty:
        random_index = random.choice(unrated_jokes.index.tolist())
        selected_joke = unrated_jokes.loc[random_index]

        return selected_joke


@rt.message(Command('rate'))
async def do_rating(msg: Message, state: FSMContext, first=True): 
    joke_data = get_joke(msg.from_user.id)
    if joke_data is None:
        await msg.answer(lexicon['already_rated_everything'])
        return
    if first:
        await msg.answer(lexicon['started_rating'])

    text = lexicon['rating_joke'] % (joke_data['topic'], joke_data['joke'])
    await msg.answer(text, reply_markup=rating_keyboard)
    await state.set_state(RatingJoke.waiting_for_rating)
    await state.set_data({'joke': joke_data['joke'], 'topic': joke_data['topic'], 'user': msg.from_user.id})


@rt.message(
    StateFilter(RatingJoke.waiting_for_rating), 
    lambda message: (message.text.isdigit() and 1 <= int(message.text) <= 10 or message.text == '/stop_rating')
)
async def handle_rating(msg: Message, state: FSMContext):
    user_data = await state.get_data()
    if msg.text == '/stop_rating':
        await msg.answer(lexicon['rating_stopped'])
        await state.clear()
        return
    rating = int(msg.text)
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO ratings (joke, user, topic, rating)
            VALUES (?, ?, ?, ?)
        """, (user_data['joke'], user_data['user'], user_data['topic'], rating))
        conn.commit()

    rated_jokes[str(user_data['user'])].append(user_data['joke'])
    rated_jokes.write()
    await do_rating(msg, state, first=False)