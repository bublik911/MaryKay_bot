from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from misc.consts import months


def month_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    for month in months:
        keyboard.button(text=month)
    keyboard.adjust(3)
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)
