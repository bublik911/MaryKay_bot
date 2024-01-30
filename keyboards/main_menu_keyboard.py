from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from misc.consts import CHECK_CLIENTS_BASE, ADD_CLIENT, SENDING


def main_menu_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text=CHECK_CLIENTS_BASE)
    keyboard.button(text=ADD_CLIENT)
    keyboard.button(text=SENDING)
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)
