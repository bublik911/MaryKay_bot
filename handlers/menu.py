from aiogram.filters import Command
from aiogram.types import Message
from handlers import add_client, check_clients
from keyboards.main_menu_keyboard import main_menu_keyboard
from aiogram import Router

router = Router()


@router.message(Command("menu"))
async def main_menu(message: Message):
    await message.answer("Что вы хотите сделать?",
                         reply_markup=main_menu_keyboard())
    router.include_routers(check_clients.router, add_client.router)
