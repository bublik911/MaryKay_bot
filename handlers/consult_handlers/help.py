from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from keyboards.url_admin_keyboard import url_admin_keyboard
router = Router()


@router.message(Command("help"))
async def help_handler(message: Message):
    await message.answer("Чтобы получить помощь по пользованию ботом, напишите администратору",
                         reply_markup=url_admin_keyboard())
