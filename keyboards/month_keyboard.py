from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def month_keyboard() -> ReplyKeyboardMarkup:
    months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]
    keyboard = ReplyKeyboardBuilder()
    for month in months:
        keyboard.button(text=month)
    keyboard.adjust(3)
    return keyboard.as_markup(resize_keyboard=True)
