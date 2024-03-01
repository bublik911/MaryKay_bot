import os

import aiogram.exceptions

from handlers import consult_handlers

from middlewares.media_group_middleware import DownloadPhotoMiddleware

from aiogram import Bot
from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, FSInputFile
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.media_group import MediaGroupBuilder

from misc.utils import all_sending
from misc.consts import SENDING, ALL_SENDING, SEND, CHANGE, BIRTHDAY_SENDING, EXCELLENT

import DataBase
from DataBase.repositories import ConsultantRepository
from DataBase import files

from states import Sending

from keyboards.url_admin_keyboard import url_admin_keyboard
from keyboards.change_keyboard import change_keyboard
from keyboards.send_type_keyboard import send_type_keyboard
from keyboards.all_type_check_keyboard import send_all_type_keyboard
from keyboards.birthday_type_check_keyboard import send_birthday_type_keyboard


client_bot = Bot(token=os.getenv('CLIENT_TOKEN'))
consult_bot = Bot(token=os.getenv('CONSULT_TOKEN'))

router = Router()
router.message.middleware(middleware=DownloadPhotoMiddleware())


@router.message(
    F.text == SENDING,
    Sending.transition
)
async def sending_start(message: Message, state: FSMContext):
    await message.answer("Сообщение какой рассылки вы хотите задать?",
                         reply_markup=send_type_keyboard())
    await state.set_state(Sending.choose)


@router.message(
    F.text == ALL_SENDING,
    Sending.choose
)
async def all_send(message: Message, state: FSMContext):
    photo_list = DataBase.files.get_photo_for_all_message(message.chat.id)
    text = ConsultantRepository.get_all_message(message)
    await message.answer("Сейчас сообщение для рассылки всем клиентам выглядит так:\n\n"
                         "Здравствуйте, <имя клиента>\n"
                         f"_{text}_",
                         reply_markup=send_all_type_keyboard(),
                         parse_mode=ParseMode.MARKDOWN)

    if len(photo_list) != 0:
        media = MediaGroupBuilder(caption="Также к сообщению будут прикреплены эти фото")
        for photo in reversed(photo_list):
            ph = FSInputFile(photo)
            media.add_photo(media=ph)
        try:
            await consult_bot.send_media_group(message.chat.id, media=media.build(),)
        except aiogram.exceptions.TelegramBadRequest:
            await message.answer("Ошибка отправки фото. Обратитесь к администратору",
                                 reply_markup=url_admin_keyboard())
    await state.set_state(Sending.all)


@router.message(
    F.text == SEND,
    Sending.all
)
async def send(message: Message, state: FSMContext):
    text = ConsultantRepository.get_all_message(message)
    await all_sending(client_bot, message, text)
    await consult_handlers.menu.main_menu(message, state)


@router.message(
    F.text == CHANGE,
    Sending.all
)
@router.message(
    F.text == CHANGE,
    Sending.all_edit_start
)
async def edit_start(message: Message, state: FSMContext):
    await message.answer("Что вы хотите изменить?",
                         reply_markup=change_keyboard())
    await state.set_state(Sending.all_edit_start)


@router.message(
    F.text == "Текст",
    Sending.all_edit_start
)
async def text(message: Message, state: FSMContext):
    await message.answer("Введите текст нового сообщения:")
    await state.set_state(Sending.all_text_edit)


@router.message(
    Sending.all_text_edit
)
async def text_edit(message: Message, state: FSMContext):
    await state.set_state(Sending.all_edited)
    ConsultantRepository.update_all_message(message)
    await all_send(message, state)


@router.message(
    F.text == "Фото",
    Sending.all_edit_start
)
async def photo(message: Message, state: FSMContext):
    await message.answer("Пришлите фотографии, которые хотите прикрепить к сообщению.\n"
                         "Внимание! Число фото в сообщении ограничено: макс. 10 шт.")
    await state.set_state(Sending.all_photo_edit)


@router.message(
    Sending.all_photo_edit
)
async def photo_edit(message: Message, state: FSMContext, album: list[Message]):
    await state.set_state(Sending.all_edited)
    files.clear_photos(message, "all")
    for msg in album:
        file_id = msg.photo[-1].file_id
        path = files.download_photo_path(msg, "all")
        await consult_bot.download(file=file_id, destination=path)
    await all_send(message, state)


@router.message(
    F.text == BIRTHDAY_SENDING,
    Sending.choose
)
@router.message(
    Sending.birthday_edited
)
async def birthday_send(message: Message, state: FSMContext):
    photo_list = DataBase.files.get_photo_for_birthday_message(message.chat.id)
    text = ConsultantRepository.get_birthday_message(message)
    await message.answer("Сейчас сообщение для рассылки клиентам ко дню рождения выглядит так:\n\n"
                         "<Имя клиента>!\n"
                         f"_{text}_",
                         reply_markup=send_birthday_type_keyboard(),
                         parse_mode=ParseMode.MARKDOWN)

    if len(photo_list) != 0:
        media = MediaGroupBuilder(caption="Также к сообщению будут прикреплены эти фото")
        for photo in reversed(photo_list):
            ph = FSInputFile(photo)
            media.add_photo(media=ph)
        try:
            await consult_bot.send_media_group(message.chat.id, media=media.build(), )
        except aiogram.exceptions.TelegramBadRequest:
            await message.answer("Ошибка отправки фото. Обратитесь к администратору",
                                 reply_markup=url_admin_keyboard())
    await state.set_state(Sending.birthday)


@router.message(
    F.text == EXCELLENT,
    Sending.birthday
)
async def commit(message: Message, state: FSMContext):
    await state.clear()
    await consult_handlers.menu.main_menu(message, state)


@router.message(
    F.text == CHANGE,
    Sending.birthday
)
@router.message(
    F.text == CHANGE,
    Sending.birthday_edit_start
)
async def birthday_edit_start(message: Message, state: FSMContext):
    await message.answer("Что вы хотите изменить?",
                         reply_markup=change_keyboard())
    await state.set_state(Sending.birthday_edit_start)


@router.message(
    F.text == "Текст",
    Sending.birthday_edit_start
)
async def text(message: Message, state: FSMContext):
    await message.answer("Введите текст нового сообщения:")
    await state.set_state(Sending.birthday_text_edit)


@router.message(
    Sending.birthday_text_edit
)
async def birthday_edit(message: Message, state: FSMContext):
    await state.set_state(Sending.birthday_edited)
    ConsultantRepository.update_birthday_message(message)
    await birthday_send(message, state)


@router.message(
    F.text == "Фото",
    Sending.birthday_edit_start
)
async def photo(message: Message, state: FSMContext):
    await message.answer("Пришлите фотографии, которые хотите прикрепить к сообщению.\n"
                         "Внимание! Число фото в сообщении ограничено: макс. 10 шт.")
    await state.set_state(Sending.birthday_photo_edit)


@router.message(
    Sending.birthday_photo_edit
)
async def photo_edit(message: Message, state: FSMContext, album: list[Message]):
    await state.set_state(Sending.birthday_edited)
    files.clear_photos(message, "birthday")
    for msg in album:
        file_id = msg.photo[-1].file_id
        path = files.download_photo_path(msg, "birthday")
        await consult_bot.download(file=file_id, destination=path)
    await birthday_send(message, state)

