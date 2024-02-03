from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from misc.consts import ALL_OK_WITH_MARK, FILL_AGAIN


def check_client_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=ALL_OK_WITH_MARK)
    keyboard.button(text=FILL_AGAIN)
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)
