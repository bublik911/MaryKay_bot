from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from misc.consts import SEND, CHANGE


def send_all_type_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=SEND)
    keyboard.button(text=CHANGE)
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)

