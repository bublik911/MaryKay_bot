from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from keyboards.url_admin_keyboard import url_admin_keyboard

from states import Start

from misc.utils import phone_parse

from DataBase.repositories import ClientRepository

router = Router()


@router.message(Command("start"))
async def authorization(message: Message, state: FSMContext):
    await message.answer(f"Здравствуйте, {message.from_user.first_name}! \n"
                         f"Здесь Вы сможете получать сообщения от консультанта компании MaryKay"
                         f" Если вам нужна помощь, обратитесь к нашему администратору. Он сможет вам помочь!",
                         reply_markup=url_admin_keyboard())
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

