from datetime import date
from DataBase.config import *
from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from states import CheckBase
from keyboards.check_clients_keyboard import check_clients_keyboard
from misc.utils import phone_parse, create_clients_list
from handlers.menu import main_menu

from DataBase.repositories import ClientRepository
router = Router()


@router.message(
    Text("📕 Проверить клиентскую базу")
)
async def check_base(message: Message, state: FSMContext):
    await state.set_state(CheckBase.start)
    await message.answer("\n".join(create_clients_list(message)),
                         reply_markup=check_clients_keyboard())


@router.message(
    Text("✅ Всё верно"),
    CheckBase.start
)
@router.message(
    CheckBase.check
)
async def all_ok(message: Message, state: FSMContext):
    await state.clear()
    await main_menu(message=message)


@router.message(
    Text("🗑 Удалить клиента из базы"),
    CheckBase.start
)
@router.message(
    Text("🗑 Удалить клиента из базы"),
    CheckBase.check
)
async def delete(message: Message, state: FSMContext):
    await state.set_state(CheckBase.delete)
    await message.answer("Введите номер телефона клиента, которого хотите удалить",
                         reply_markup=ReplyKeyboardRemove())


@router.message(
    CheckBase.delete
)
async def delete_commit(message: Message, state: FSMContext):
    response = ClientRepository.delete_client(phone_parse(message.text))
    if response == 0:
        await message.answer("Такого клиента не существует, проверьте список, пожалуйста")
        await message.answer("\n".join(create_clients_list(message)),
                             reply_markup=check_clients_keyboard())
    else:
        await message.answer("Клиент удален. Это обновленный список клиентов")
        await message.answer("\n".join(create_clients_list(message)),
                             reply_markup=check_clients_keyboard())
    await state.set_state(CheckBase.check)

