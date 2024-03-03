from handlers import consult_handlers

from aiogram import Router, F
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import ReplyKeyboardRemove

from DataBase.repositories import ClientRepository
from DataBase.repositories import ConsultantRepository

from states import CheckBase, DeleteClient

from keyboards.yes_no_keyboard import yes_no_keyboard

from misc.consts import DELETE_CLIENT, YES, NO

router = Router()


@router.message(
    Command("delete_client")
)
async def delete_start(message: Message, state: FSMContext):
    await state.clear()
    await consult_handlers.check_clients.check_base(message, state)
    await message.answer("Введите номер клиента в таблице для удаления",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(DeleteClient.confirm)


@router.message(
    F.text == DELETE_CLIENT,
    DeleteClient.transition
)
async def start(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Введите номер клиента в таблице для удаления",
                         reply_markup=ReplyKeyboardRemove())
    await state.set_state(DeleteClient.confirm)


@router.message(
    DeleteClient.confirm
)
async def confirm(message: Message, state: FSMContext):
    number = message.text
    pid = ConsultantRepository.get_consultant_id_by_chat_id(message.chat.id)
    clients = ClientRepository.get_clients_list_by_pid(pid)
    await state.update_data(number=int(number))
    i = 1
    for client in clients:
        if int(number) == i:
            phone_number = client.phone
            id = ClientRepository.get_id_by_phone_number_and_pid(phone_number, pid)
            await message.answer(f"Удалить клиента {client.name}?",
                                 reply_markup=yes_no_keyboard())
        i += 1
    await state.set_state(DeleteClient.commit)


@router.message(
    F.text == YES,
    DeleteClient.commit
)
async def delete_commit(message: Message, state: FSMContext):
    data = await state.get_data()
    number = data['number']
    pid = ConsultantRepository.get_consultant_id_by_chat_id(message.chat.id)
    clients = ClientRepository.get_clients_list_by_pid(pid)

    i = 1
    for client in clients:
        if int(number) == i:
            phone_number = client.phone
            id = ClientRepository.get_id_by_phone_number_and_pid(phone_number, pid)
            await message.answer(f"Клиент {client.name} удален")
            ClientRepository.delete_by_id(id)
            break
        i += 1
    await state.set_state(CheckBase.transition)
    await message.answer("Таблица изменена:")
    await consult_handlers.check_clients.check_base(message, state)


@router.message(
    F.text == NO,
    DeleteClient.commit
)
async def return_to_check(message: Message, state: FSMContext):
    await consult_handlers.check_clients.check_base(message, state)
