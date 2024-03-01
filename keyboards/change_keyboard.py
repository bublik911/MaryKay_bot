from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def change_keyboard() -> ReplyKeyboardMarkup:
    kb = ReplyKeyboardBuilder()
    kb.button(text="Текст")
    kb.button(text="Фото")
    return kb.as_markup(resize_keyboard=True,
                        one_time_keyboard=True)