from aiogram.fsm.state import State, StatesGroup


class AddingJoke(StatesGroup):
    waiting_for_topic = State()
    waiting_for_joke = State()

class Joke(StatesGroup):
    new_joke = State()
    rating = State()

class MemeMaking(StatesGroup):
    waiting_for_style = State()

class RatingJoke(StatesGroup):
    waiting_for_rating = State()