from DataBase.config import *
from aiogram import Bot
from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Text
from aiogram.types import Message
from misc import env
from misc.utils import create_send_list
from states import Sending
from keyboards.send_type_keyboard import send_type_keyboard
from keyboards.all_type_check_keyboard import send_all_type_keyboard
from keyboards.birthday_type_check_keyboard import send_birthday_type_keyboard
from handlers.menu import main_menu
bot = Bot(token=env.TgKeys.TOKEN)
router = Router()


@router.message(
    Text("✉ Рассылка")
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
    db.connect(reuse_if_open=True)
    text = Consultant.get(Consultant.chat_id == message.chat.id).all_message
    await message.answer("Сейчас сообщение для рассылки всем клиентам выглядит так:\n"
                         "Здравствуйте, <имя клиента>"
                         f"{text}",
                         reply_markup=send_all_type_keyboard())
    await state.set_state(Sending.all)
    db.close()


@router.message(
    Text("📨 Отправить"),
    Sending.all
)
async def send(message: Message, state: FSMContext):
    db.connect(reuse_if_open=True)
    text = Consultant.get(Consultant.chat_id == message.chat.id).all_message
    for client in create_send_list(message):
        await bot.send_message(chat_id=client[0], text=f"Здравствуйте, {client[1]}!")
        await bot.send_message(chat_id=client[0], text=text)
    await message.answer("Рассылка произведена:")
    await message.answer("\n".join(str(cli[1]) for cli in create_send_list(message)))
    db.close()
    await state.clear()
    await main_menu(message=message)


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
    db.connect(reuse_if_open=True)
    Consultant.update(all_message=message.text).where(Consultant.chat_id == message.chat.id).execute()
    db.close()
    await state.set_state(Sending.all_edited)
    await all_send(message, state)


@router.message(
    Text("🎁 Рассылка ко дню рождения"),
    Sending.choose
)
@router.message(
    Sending.birthday_edited
)
async def birthday_send(message: Message, state: FSMContext):
    db.connect(reuse_if_open=True)
    text = Consultant.get(Consultant.chat_id == message.chat.id).birthday_message
    await message.answer("Сейчас сообщение для рассылки клиентам ко дню рождения выглядит так:\n"
                         "Здравствуйте, <имя клиента>\n"
                         f"{text}",
                         reply_markup=send_birthday_type_keyboard())
    db.close()
    await state.set_state(Sending.birthday)


@router.message(
    Text("✅ Отлично"),
    Sending.birthday
)
async def commit(message: Message, state: FSMContext):
    await state.clear()
    await main_menu(message=message)


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
    db.connect(reuse_if_open=True)
    Consultant.update(birthday_message=message.text).where(Consultant.chat_id == message.chat.id).execute()
    db.close()
    await state.set_state(Sending.birthday_edited)
    await birthday_send(message, state)
