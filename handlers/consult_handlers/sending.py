import os

from handlers import consult_handlers

from aiogram import Bot
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from aiogram.types import Message
from aiogram.enums.parse_mode import ParseMode

from misc.utils import all_sending
from misc.consts import SENDING, ALL_SENDING, SEND, CHANGE, BIRTHDAY_SENDING, EXCELLENT

from db.repositories import ConsultantRepository

from states import Sending

from keyboards.send_type_keyboard import send_type_keyboard
from keyboards.all_type_check_keyboard import send_all_type_keyboard
from keyboards.birthday_type_check_keyboard import send_birthday_type_keyboard


bot = Bot(token=os.getenv('CLIENT_TOKEN'))
router = Router()


@router.message(
    Text(SENDING),
    Sending.transition
)
async def sending_start(message: Message, state: FSMContext):
    await message.answer("Сообщение какой рассылки вы хотите задать?",
                         reply_markup=send_type_keyboard())
    await state.set_state(Sending.choose)


@router.message(
    Text(ALL_SENDING),
    Sending.choose
)
@router.message(
    Sending.all_edited
)
async def all_send(message: Message, state: FSMContext):
    text = ConsultantRepository.get_all_message(message)
    await message.answer("Сейчас сообщение для рассылки всем клиентам выглядит так:\n\n"
                         "Здравствуйте, <имя клиента>\n"
                         f"_{text}_",
                         reply_markup=send_all_type_keyboard(),
                         parse_mode=ParseMode.MARKDOWN)
    await state.set_state(Sending.all)


@router.message(
    Text(SEND),
    Sending.all
)
async def send(message: Message, state: FSMContext):
    text = ConsultantRepository.get_all_message(message)
    await all_sending(bot, message, text)
    await consult_handlers.menu.main_menu(message, state)


@router.message(
    Text(CHANGE),
    Sending.all
)
@router.message(
    Text(CHANGE),
    Sending.all_edit_start
)
async def edit_start(message: Message, state: FSMContext):
    await message.answer("Введите текст сообщения")
    await state.set_state(Sending.all_edit_start)


@router.message(
    Sending.all_edit_start
)
async def edit(message: Message, state: FSMContext):
    await state.set_state(Sending.all_edited)
    ConsultantRepository.update_all_message(message)
    await all_send(message, state)


@router.message(
    Text(BIRTHDAY_SENDING),
    Sending.choose
)
@router.message(
    Sending.birthday_edited
)
async def birthday_send(message: Message, state: FSMContext):
    text = ConsultantRepository.get_birthday_message(message)
    await message.answer("Сейчас сообщение для рассылки клиентам ко дню рождения выглядит так:\n\n"
                         "<Имя клиента>!\n"
                         f"_{text}_",
                         reply_markup=send_birthday_type_keyboard(),
                         parse_mode=ParseMode.MARKDOWN)
    await state.set_state(Sending.birthday)


@router.message(
    Text(EXCELLENT),
    Sending.birthday
)
async def commit(message: Message, state: FSMContext):
    await state.clear()
    await consult_handlers.menu.main_menu(message, state)


@router.message(
    Text(CHANGE),
    Sending.birthday
)
@router.message(
    Text(CHANGE),
    Sending.birthday_edit_start
)
async def birthday_edit_start(message: Message, state: FSMContext):
    await message.answer("Введите текст сообщения")
    await state.set_state(Sending.birthday_edit_start)


@router.message(
    Sending.birthday_edit_start
)
async def birthday_edit(message: Message, state: FSMContext):
    await state.set_state(Sending.birthday_edited)
    ConsultantRepository.update_birthday_message(message)
    await birthday_send(message, state)
