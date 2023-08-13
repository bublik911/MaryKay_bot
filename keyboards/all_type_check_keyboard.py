from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def send_all_type_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="📨 Отправить")
    keyboard.button(text="🔄 Изменить")
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)

