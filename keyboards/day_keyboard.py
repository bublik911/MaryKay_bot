from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup

from misc.utils import month_len


def day_keyboard(month: str) -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    for day in range(1, month_len(month) + 1):
        keyboard.button(text=f"{day}")
    keyboard.adjust(6)
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)
