from aiogram import Router
from misc.utils import phone_parse, month_to_date
from aiogram.types import Message, ReplyKeyboardRemove
from aiogram.filters import Text
from aiogram.fsm.context import FSMContext
from states import AddClient
from keyboards.month_keyboard import month_keyboard
from keyboards.day_keyboard import day_keyboard
from keyboards.check_client_keyboard import check_client_keyboard
from handlers.menu import main_menu

from DataBase.repositories import ClientRepository, ConsultantRepository

router = Router()


@router.message(
    Text("✏ Добавить клиента")
)
async def start(message: Message, state: FSMContext):
    await message.answer("Введите имя клиента")
    await state.set_state(AddClient.name)


@router.message(
    AddClient.name
)
async def add_client_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text, chat_id=message.chat.id)
    await message.answer("Введите номер телефона клиента")
    await state.set_state(AddClient.phone)


@router.message(
    AddClient.phone
)
async def add_client_phone(message: Message, state: FSMContext):
    await state.update_data(phone=phone_parse(message.text))
    await message.answer("Выберете месяц рождения клиента",
                         reply_markup=month_keyboard())
    await state.set_state(AddClient.month)


@router.message(
    AddClient.month
)
async def add_client_month(message: Message, state: FSMContext):
    await state.update_data(month=month_to_date(message.text))
    await message.answer("Выберете дату рождения клиента",
                         reply_markup=day_keyboard())
    await state.set_state(AddClient.day)


@router.message(
    AddClient.day
)
async def add_client_day(message: Message, state: FSMContext):
    await state.update_data(day=message.text)
    client = await state.get_data()
    await message.answer("Хотите добавить клиента со следующими параметрами?")
    await message.answer(f"Имя: {client['name']}\n"
                         f"Телефон: +7{client['phone']}\n"
                         f"Дата рождения: {client['month']}-{client['day']}",
                         reply_markup=check_client_keyboard())
    await state.set_state(AddClient.commit)


@router.message(
    AddClient.commit,
    Text("✅ Да")
)
async def commit(message: Message, state: FSMContext):
    pid = ConsultantRepository.get_consultant_id_by_chat_id(message.chat.id)
    await ClientRepository.create_client(state, pid)
    await main_menu(message, state)


@router.message(
    AddClient.commit,
    Text("🔄 Заполнить заново")
)
async def again(message: Message, state: FSMContext):
    await state.clear()
    await state.set_state(AddClient.name)
    await message.answer("Введите имя клиента",
                         reply_markup=ReplyKeyboardRemove())
