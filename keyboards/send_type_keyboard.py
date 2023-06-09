from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def send_type_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Рассылка всем")
    keyboard.button(text="Рассылка ко дню рождения")
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)
