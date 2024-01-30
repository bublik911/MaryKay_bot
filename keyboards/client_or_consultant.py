from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from misc.consts import CLIENT, CONSULTANT


def client_or_consultant() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=CLIENT)
    keyboard.button(text=CONSULTANT)
    return keyboard.as_markup(one_time_keyboard=True,
                              resize_keyboard=True)
