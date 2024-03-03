from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def delete_photos() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Удалить фотографии")
    return keyboard.as_markup(one_time_keyboard=True,
                              resize_keyboard=True)
