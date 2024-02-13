import handlers.consult_handlers
from DataBase.config import *
from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, Text
from aiogram.fsm.context import FSMContext
from keyboards.url_admin_keyboard import url_admin_keyboard
from keyboards.client_or_consultant import client_or_consultant
from keyboards.main_menu_keyboard import main_menu_keyboard
from states import Start

from misc.utils import phone_parse
from misc.consts import CLIENT, CONSULTANT

from DataBase.repositories import ConsultantRepository, ClientRepository
router = Router()


@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(f"Здравствуйте, {message.from_user.first_name}! "
                         f"Я буду помогать Вам делать рассылку клиентам, работающих с Вами!"
                         f" Если вам нужна помощь, обратитесь к нашему администратору. Он сможет вам помочь!",
                         reply_markup=url_admin_keyboard())
    await message.answer("Вы клиент или консультант?",
                         reply_markup=client_or_consultant())


@router.message(
    Text(CLIENT)
)
async def client(message: Message, state: FSMContext):
    await message.answer("Введите свой номер телефона")
    await state.set_state(Start.client)


@router.message(
    Start.client
)
async def client_check_finish(message: Message, state: FSMContext):
    if len(phone_parse(message.text)) < 10:
        await message.answer("Введите корректный номер. Например: 8-(777)-777-77-77")
    else:
        if ClientRepository.count_clients_by_phone(phone_parse(message.text)) == 0:
            await message.answer("Вашего номера нет в базе клиентов.\n"
                                 "Обратитесь к своему консультанту или администратору, чтобы вас добавили в базу",
                                 reply_markup=url_admin_keyboard())
        else:
            ClientRepository.update_client_chat_id_by_phone(message.chat.id, phone_parse(message.text))
            await message.answer("Отлично! Теперь вы будете получать информацию от своего консультанта!")
            await state.clear()


@router.message(
    Text(CONSULTANT)
)
async def consultant(message: Message, state: FSMContext):
    await message.answer("Введите свой номер телефона")
    await state.set_state(Start.consultant)


@router.message(
    Start.consultant
)
async def consultant_check_finish(message: Message, state: FSMContext):
    if len(phone_parse(message.text)) < 10:
        await message.answer("Введите корректный номер. Например: 8-(777)-777-77-77")
    else:
        if ConsultantRepository.count_consultants_by_phone(phone_parse(message.text)) == 0:
            await message.answer("Вашего номера нет в базе консультантов.\n"
                                 "Обратитесь к администратору, чтобы вас добавили в базу",
                                 reply_markup=url_admin_keyboard())
        else:
            ConsultantRepository.update_consultant_chat_id_by_phone(message.chat.id, phone_parse(message.text))
            await message.answer("Что вы хотите сделать?", reply_markup=main_menu_keyboard())
            await state.clear()
    # router.include_routers(check_clients.router, add_client.router, sending.router)

