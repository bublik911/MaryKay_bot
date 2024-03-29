import prettytable
from handlers import consult_handlers

from aiogram import Router, F
from aiogram.enums.parse_mode import ParseMode
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from DataBase.repositories import ClientRepository
from DataBase.repositories import ConsultantRepository

from states import CheckBase, DeleteClient, Menu, AddClient

from keyboards.check_clients_keyboard import check_clients_keyboard

from misc.consts import CHECK_CLIENTS_BASE, OK_WITH_MARK, DELETE_CLIENT, ADD_CLIENT
from misc.utils import date_to_month, correct_date


router = Router()


@router.message(
    Command("check_clients")
)
@router.message(
    F.text == CHECK_CLIENTS_BASE
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
    table.align = 'l'
    table._max_width = {"Данные о клиенте": 25}
    i = 1
    for client in clients:
        table.add_row([i, client.name + "\n" +
                       "+7" + client.phone + "\n" +
                       correct_date(str(client.date.day)) + " " + date_to_month(client.date.month) + "\n"])
        if i % 10 == 0:
            await message.answer(f"`{table}`",
                                 parse_mode=ParseMode.MARKDOWN,
                                 reply_markup=check_clients_keyboard())
            table.clear_rows()
        i += 1
    if len(table.rows) == 0 and i == 1:
        await message.answer("Таблица пуста")
        await consult_handlers.menu.main_menu(message, state)
    elif i % 10 == 1:
        await state.set_state(CheckBase.waiting)
    else:
        await message.answer(f"`{table}`",
                             parse_mode=ParseMode.MARKDOWN,
                             reply_markup=check_clients_keyboard())
        await state.set_state(CheckBase.waiting)


@router.message(
    CheckBase.waiting
)
async def answer_routing(message: Message, state: FSMContext):
    if message.text == OK_WITH_MARK:
        await state.set_state(Menu.transition)
        await consult_handlers.menu.main_menu(message, state)

    elif message.text == DELETE_CLIENT:
        await state.set_state(DeleteClient.transition)
        await consult_handlers.delete_client.start(message, state)

    elif message.text == ADD_CLIENT:
        await state.set_state(AddClient.transition)
        await consult_handlers.add_client.start(message, state)


