from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command, Text
from keyboards.url_admin_keyboard import url_admin_keyboard
from keyboards.client_or_consultant import client_or_consultant
from keyboards.main_menu_keyboard import main_menu_keyboard
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from handlers import add_client, check_clients, sending
from utils import phone_parse
from DataBase.models_db import *

router = Router()


# отредачить сообщение
@router.message(Command("start"))
async def start_handler(message: Message):
    await message.answer(f"Здравствуйте, {message.from_user.first_name}! "
                         f"Я буду помогать Вам делать рассылку клиентам, работающих с Вами!"
                         f" Если вам нужна помощь, обратитесь к нашему администратору. Он сможет вам помочь!",
                         reply_markup=url_admin_keyboard())
    await message.answer("Вы клиент или консультант?",
                         reply_markup=client_or_consultant())


class Phone(StatesGroup):
    client = State()
    consultant = State()


@router.message(
    Text("Клиент")
)
async def client(message: Message, state: FSMContext):
    await message.answer("Введите свой номер телефона")
    await state.set_state(Phone.client)


@router.message(
    Phone.client
)
async def client_check_finish(message: Message, state: FSMContext):
    if len(phone_parse(message.text)) < 10:
        await message.answer("Введите корректный номер. Например: 8-(777)-777-77-77")
    else:
        if Client.select().where(Client.phone == phone_parse(message.text)).count() == 0:
            await message.answer("Вашего номера нет в базе клиентов.\n"
                                 "Обратитесь к своему консультанту или администратору, чтобы вас добавили в базу",
                                 reply_markup=url_admin_keyboard())
        else:
            Client.update(chat_id=message.chat.id).where(Client.phone == phone_parse(message.text)).execute()
            await message.answer("Отлично! Теперь вы будете получать информацию от своего консультанта!")
            await state.clear()


@router.message(
    Text("Консультант")
)
async def consultant(message: Message, state: FSMContext):
    await message.answer("Введите свой номер телефона")
    await state.set_state(Phone.consultant)


@router.message(
    Phone.consultant
)
async def consultant_check_finish(message: Message, state: FSMContext):
    if len(phone_parse(message.text)) < 10:
        await message.answer("Введите корректный номер. Например: 8-(777)-777-77-77")
    else:
        if Consultant.select().where(Consultant.phone == phone_parse(message.text)).count() == 0:
            await message.answer("Вашего номера нет в базе консультантов.\n"
                                 "Обратитесь к администратору, чтобы вас добавили в базу",
                                 reply_markup=url_admin_keyboard())
        else:
            Consultant.update(chat_id=message.chat.id).where(Consultant.phone == phone_parse(message.text)).execute()
            await message.answer("Что вы хотите сделать?", reply_markup=main_menu_keyboard())
            await state.clear()
    router.include_routers(check_clients.router, add_client.router, sending.router)

