from datetime import date
from DataBase.models_db import *
from aiogram import Router
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from states import CheckBase
from keyboards.check_clients_keyboard import check_clients_keyboard
from misc.utils import phone_parse, create_clients_list
from handlers.menu import main_menu
router = Router()


@router.message(
    Text("📕Проверить клиентскую базу")
)
async def check_base(message: Message, state: FSMContext):
    await state.set_state(CheckBase.start)
    await message.answer("\n".join(create_clients_list(message)),
                         reply_markup=check_clients_keyboard())


@router.message(
    Text("Всё верно"),
    CheckBase.start
)
@router.message(
    CheckBase.check
)
async def all_ok(message: Message, state: FSMContext):
    await state.clear()
    await main_menu(message=message)


@router.message(
    Text("Удалить клиента из базы"),
    CheckBase.start
)
@router.message(
    Text("Удалить клиента из базы"),
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
    db.connect(reuse_if_open=True)
    Client.update(deleted_at=date.today()).where((Client.phone == phone_parse(message.text)) & (Client.deleted_at.is_null())).execute()
    db.close()
    await state.set_state(CheckBase.check)
    await message.answer("Клиент удален. Это обновленный список клиентов")
    await message.answer("\n".join(create_clients_list(message)),
                         reply_markup=check_clients_keyboard())
