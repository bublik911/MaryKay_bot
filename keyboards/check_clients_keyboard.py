from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram.types import ReplyKeyboardMarkup


def check_clients_keyboard() -> ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()
    keyboard.button(text="Всё верно")
    keyboard.button(text="Удалить клиента из базы")
    return keyboard.as_markup(resize_keyboard=True,
                              one_time_keyboard=True)
