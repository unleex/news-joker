from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton
RATING_SCALE = range(1, 10 + 1)
kb = []
for mark in RATING_SCALE:
    btn = InlineKeyboardButton(
        text=str(mark),
        callback_data=f"rating_{mark}"
    )
    kb.append([btn])

rating_keyboard = InlineKeyboardMarkup(
    inline_keyboard=kb,
    resize_keyboard=True
)


# Create buttons 1-10
buttons = [KeyboardButton(text=str(i)) for i in range(1, 11)]

# Create keyboard with all buttons in one row
rating_keyboard = ReplyKeyboardMarkup(
    keyboard=[buttons],
    resize_keyboard=True,
    one_time_keyboard=True  # hides keyboard after selection
)