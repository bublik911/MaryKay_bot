from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from misc.consts import ALL_OK, ADD_CLIENT, DELETE_CLIENT


def check_clients_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=ALL_OK)
    keyboard.button(text=ADD_CLIENT)
    keyboard.button(text=DELETE_CLIENT)
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)
