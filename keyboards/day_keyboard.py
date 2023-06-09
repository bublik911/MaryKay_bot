from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def day_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    for day in range(1, 32):
        keyboard.button(text=f"{day}")
    keyboard.adjust(6)
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)
