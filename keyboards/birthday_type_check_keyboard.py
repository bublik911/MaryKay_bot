from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def send_birthday_type_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Отлично")
    keyboard.button(text="Изменить")
    return keyboard.as_markup(resize_keyboard=True)
