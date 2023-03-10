from aiogram.filters import Command
from aiogram.types import Message
from keyboards.main_menu_keyboard import main_menu_keyboard
from aiogram import Router

router = Router()


@router.message(Command("menu"))
async def main_menu(message: Message):
    await message.answer("Что вы хотите сделать?",
                         reply_markup=main_menu_keyboard())
