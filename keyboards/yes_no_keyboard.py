from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from misc.consts import YES, NO


def yes_no_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=YES)
    keyboard.button(text=NO)
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)
