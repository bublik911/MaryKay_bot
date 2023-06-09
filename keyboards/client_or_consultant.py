from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def client_or_consultant() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Клиент")
    keyboard.button(text="Консультант")
    return keyboard.as_markup(one_time_keyboard=True,
                              resize_keyboard=True)
