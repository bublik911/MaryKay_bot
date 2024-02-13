import handlers

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.filters import Command
from aiogram.types import Message

from states import Menu, CheckBase, AddClient, Sending

from keyboards.main_menu_keyboard import main_menu_keyboard

from misc.consts import CHECK_CLIENTS_BASE, ADD_CLIENT, SENDING


router = Router()


@router.message(
    Command("menu")
)
@router.message(
    Menu.transition
)
async def main_menu(message: Message, state: FSMContext):
    await state.clear()
    await message.answer("Что вы хотите сделать?",
                         reply_markup=main_menu_keyboard())
    await state.set_state(Menu.waiting)


@router.message(
    Menu.waiting
)
async def answer_routing(message: Message, state: FSMContext):

    if message.text == CHECK_CLIENTS_BASE:
        await state.set_state(CheckBase.transition)
        await handlers.check_clients.check_base(message, state)

    elif message.text == ADD_CLIENT:
        await state.set_state(AddClient.transition)
        await handlers.add_client.start(message, state)

    elif message.text == SENDING:
        await state.set_state(Sending.transition)
        await handlers.sending.sending_start(message, state)
