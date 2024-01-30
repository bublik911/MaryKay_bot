import prettytable
import handlers

from aiogram import Router
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext

from DataBase.repositories import ClientRepository
from DataBase.repositories import ConsultantRepository

from states import CheckBase, DeleteClient, Menu, AddClient

from keyboards.check_clients_keyboard import check_clients_keyboard

from misc.consts import CHECK_CLIENTS_BASE, ALL_OK, DELETE_CLIENT, ADD_CLIENT
from misc.utils import date_to_month


router = Router()


@router.message(
    Text(CHECK_CLIENTS_BASE)
)
@router.message(
    CheckBase.transition
)
async def check_base(message: Message, state: FSMContext):
    await state.clear()
    pid = ConsultantRepository.get_consultant_id_by_chat_id(message.chat.id)
    clients = ClientRepository.get_clients_list_by_pid(pid)

    table = prettytable.PrettyTable()
    table.field_names = ["№", "Данные о клиенте"]
    table.align = 'c'
    i = 1
    for client in clients:
        table.add_row([i, client.name + "\n" +
                       "+7" + client.phone + "\n" +
                       str(client.date.day) + " " + date_to_month(client.date.month)])
        i += 1
    if len(table.rows) == 0:
        await message.answer("Таблица пуста")
    else:
        await message.answer(f"```{table}```",
                             parse_mode=ParseMode.MARKDOWN_V2)
        await message.answer("Всё верно?",
                             reply_markup=check_clients_keyboard())
    await state.set_state(CheckBase.waiting)


@router.message(
    CheckBase.waiting
)
async def answer_routing(message: Message, state: FSMContext):
    if message.text == ALL_OK:
        await state.set_state(Menu.transition)
        await handlers.menu.main_menu(message, state)

    elif message.text == DELETE_CLIENT:
        await state.set_state(DeleteClient.transition)
        await handlers.delete_client.start(message, state)

    elif message.text == ADD_CLIENT:
        await state.set_state(AddClient.transition)
        await handlers.add_client.start(message, state)


