from handlers import consult_handlers

from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from keyboards.url_admin_keyboard import url_admin_keyboard
from keyboards.main_menu_keyboard import main_menu_keyboard
from states import Start

from misc.utils import phone_parse

from db.repositories import ConsultantRepository
router = Router()


@router.message(Command("start"))
async def start_handler(message: Message, state: FSMContext):
    await message.answer(f"Здравствуйте, {message.from_user.first_name}! "
                         f"Я буду помогать Вам делать рассылку клиентам, работающих с Вами!"
                         f" Если вам нужна помощь, обратитесь к нашему администратору. Он сможет вам помочь!",
                         reply_markup=url_admin_keyboard())
    await message.answer("Введите свой номер телефона")
    await state.set_state(Start.waiting)


@router.message(
    Start.waiting
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
            await consult_handlers.menu.main_menu(message, state)
