from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def check_client_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="✅ Да")
    keyboard.button(text="🔄 Заполнить заново")
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)
