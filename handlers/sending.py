import handlers

from aiogram import Bot
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from aiogram.types import Message

from misc import env
from misc.utils import create_send_list
from misc.consts import SENDING

from DataBase.repositories import ConsultantRepository

from states import Sending

from keyboards.send_type_keyboard import send_type_keyboard
from keyboards.all_type_check_keyboard import send_all_type_keyboard
from keyboards.birthday_type_check_keyboard import send_birthday_type_keyboard


bot = Bot(token=env.TgKeys.TOKEN)
router = Router()


@router.message(
    Text(SENDING),
    Sending.transition
)
async def sending_start(message: Message, state: FSMContext):
    await message.answer("Параметры какой рассылки вы хотите задать?",
                         reply_markup=send_type_keyboard())
    await state.set_state(Sending.choose)


@router.message(
    Text("✉️ Рассылка всем"),
    Sending.choose
)
@router.message(
    Sending.all_edited
)
async def all_send(message: Message, state: FSMContext):
    text = ConsultantRepository.get_all_message(message)
    await message.answer("Сейчас сообщение для рассылки всем клиентам выглядит так:\n"
                         "Здравствуйте, <имя клиента>"
                         f"{text}",
                         reply_markup=send_all_type_keyboard())
    await state.set_state(Sending.all)


@router.message(
    Text("📨 Отправить"),
    Sending.all
)
async def send(message: Message, state: FSMContext):
    text = ConsultantRepository.get_all_message(message)
    for client in create_send_list(message):
        await bot.send_message(chat_id=client[0], text=f"Здравствуйте, {client[1]}!")
        await bot.send_message(chat_id=client[0], text=text)
    await message.answer("Рассылка произведена:")
    await message.answer("\n".join(str(cli[1]) for cli in create_send_list(message)))
    await state.clear()
    await handlers.menu.main_menu(message, state)


@router.message(
    Text("🔄 Изменить"),
    Sending.all
)
async def edit_start(message: Message, state: FSMContext):
    await message.answer("Введите новое сообщение")
    await state.set_state(Sending.all_edit_start)


@router.message(
    Sending.all_edit_start
)
async def edit(message: Message, state: FSMContext):
    await state.set_state(Sending.all_edited)
    ConsultantRepository.update_all_message(message)
    await all_send(message, state)


@router.message(
    Text("🎁 Рассылка ко дню рождения"),
    Sending.choose
)
@router.message(
    Sending.birthday_edited
)
async def birthday_send(message: Message, state: FSMContext):
    text = ConsultantRepository.get_birthday_message(message)
    await message.answer("Сейчас сообщение для рассылки клиентам ко дню рождения выглядит так:\n"
                         "Здравствуйте, <имя клиента>\n"
                         f"{text}",
                         reply_markup=send_birthday_type_keyboard())

    await state.set_state(Sending.birthday)


@router.message(
    Text("✅ Отлично"),
    Sending.birthday
)
async def commit(message: Message, state: FSMContext):
    await state.clear()
    await handlers.menu.main_menu(message, state)


@router.message(
    Text("🔄 Изменить"),
    Sending.birthday
)
async def birthday_edit_start(message: Message, state: FSMContext):
    await message.answer("Введите новое сообщение")
    await state.set_state(Sending.birthday_edit_start)


@router.message(
    Sending.birthday_edit_start
)
async def birthday_edit(message: Message, state: FSMContext):
    await state.set_state(Sending.birthday_edited)
    ConsultantRepository.update_birthday_message(message)
    await birthday_send(message, state)
