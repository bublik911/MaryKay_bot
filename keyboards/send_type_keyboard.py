from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from misc.consts import ALL_SENDING, BIRTHDAY_SENDING


def send_type_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=ALL_SENDING)
    keyboard.button(text=BIRTHDAY_SENDING)
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)
