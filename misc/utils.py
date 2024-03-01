import aiogram.exceptions
import prettytable

from datetime import date

from aiogram import Bot
from aiogram.types import Message, FSInputFile
from aiogram.enums.parse_mode import ParseMode
from aiogram.utils.media_group import MediaGroupBuilder

import DataBase.files
from misc.consts import months, response_months, days_in_month

from keyboards.url_admin_keyboard import url_admin_keyboard
from keyboards.main_menu_keyboard import main_menu_keyboard

from DataBase.repositories import ConsultantRepository, ClientRepository


def month_len(month: str) -> int:
    if month in days_in_month:
        return days_in_month.get(month)
    else:
        return 31


def phone_parse(x) -> str:
    s = str(x)
    phone = ''
    for i in s:
        if i.isdigit():
            phone += i
    phone = phone[-10:]
    return phone


def month_to_date(month) -> int or bool:
    if month in months:
        if months.index(month) == 0:
            return 1
        elif months.index(month) == 11:
            return 12
        else:
            return months.index(month) + 1
    return False


def date_to_month(data) -> str:
    if int(data) >= 1 and int(data) <= 12:
        return response_months[int(data) - 1]


def correct_date(data: str) -> str:
    if int(data) < 10:
        return "0" + data
    return data


def create_send_list(message: Message, null_chat_id: bool):
    pid = ConsultantRepository.get_consultant_id_by_chat_id(message.chat.id)
    clients = ClientRepository.get_clients_list_by_pid_chat_id(pid, null_chat_id)
    response = []
    for client in clients:
        response.append(client)
    return response


async def send_all_message_to_client(bot: Bot, consultant_chat_id: int, client_chat_id: int, name: str, text: str):
    photo_list = DataBase.files.get_photo_for_all_message(consultant_chat_id)
    if len(photo_list) == 0:
        await bot.send_message(client_chat_id, f"Здравствуйте! {name}\n" + text)
    else:
        media = MediaGroupBuilder(caption=f"Здравствуйте! {name}\n" + text)
        for photo in photo_list:
            ph = FSInputFile(photo)
            media.add_photo(media=ph)
        await bot.send_media_group(client_chat_id, media=media.build())


async def send_birthday_message_to_client(bot: Bot, consultant_chat_id: int, client_chat_id: int, name: str, text: str):
    photo_list = DataBase.files.get_photo_for_birthday_message(consultant_chat_id)
    if len(photo_list) == 0:
        await bot.send_message(client_chat_id, f"{name}! \n" + text)
    else:
        media = MediaGroupBuilder(caption=f"Здравствуйте! {name}\n" + text)
        for photo in photo_list:
            ph = FSInputFile(photo)
            media.add_photo(media=ph)
        await bot.send_media_group(client_chat_id, media=media.build())


async def all_sending(bot: Bot, message: Message, text: str):
    send_table = prettytable.PrettyTable()
    send_table.field_names = ["Имя", "Телефон"]
    send_table.align = 'l'
    send_table._max_width = {"Имя": 10}

    failed = create_send_list(message, True)
    correct = create_send_list(message, False)

    if len(correct) == 0:
        await message.answer("Ошибка рассылки. Обратитесь к администратору",
                             reply_markup=url_admin_keyboard())
    elif len(failed) + len(correct) == 0:
        await message.answer("Список рассылки пуст.",
                             reply_markup=url_admin_keyboard())
    else:
        i = 1
        await message.answer("Рассылка совершена:")
        for client in correct:
            if i % 10 == 0:
                await message.answer(f"`{send_table}`",
                                     parse_mode=ParseMode.MARKDOWN)
                send_table.clear_rows()
            try:

                await send_all_message_to_client(bot=bot,
                                                 consultant_chat_id=message.chat.id,
                                                 client_chat_id=client.chat_id,
                                                 name=client.name, text=text)

            except aiogram.exceptions.TelegramBadRequest:
                send_table.add_row([client.name, "+7" + client.phone + " ❌" + "\n"])
                i += 1
                continue
            send_table.add_row([client.name, "+7" + client.phone + " ✅" + "\n"])
            i += 1
        for client in failed:
            if i % 10 == 0:
                await message.answer(f"`{send_table}`",
                                     parse_mode=ParseMode.MARKDOWN)
                send_table.clear_rows()
            send_table.add_row([client.name, "+7" + client.phone + " ❌" + "\n"])
            i += 1
        await message.answer(f"`{send_table}`",
                             parse_mode=ParseMode.MARKDOWN)


async def birthday_sending(consult_bot: Bot, client_bot: Bot):

    send_table = prettytable.PrettyTable()
    send_table.field_names = ["Имя", "Дата рождения"]
    send_table.align = 'r'
    send_table._max_width = {"Имя": 25}

    consultants = ConsultantRepository.get_id_chat_id_birthday_message()
    for consultant in consultants:

        correct = ClientRepository.get_clients_list_by_pid_chat_id(consultant.id, False)
        failed = ClientRepository.get_clients_list_by_pid_chat_id(consultant.id, True)

        if len(correct) == 0 or len(failed) + len(correct) == 0:
            await consult_bot.send_message(consultant.chat_id, "Ошибка рассылки с поздравлением. "
                                                               "Обратитесь к администратору",
                                           reply_markup=url_admin_keyboard())
        else:
            i = 1
            for client in correct:
                date_birth_month = client.date.month
                date_birth_day = client.date.day
                today_month = date.today().month
                today_day = date.today().day

                if today_month == date_birth_month and date_birth_day - today_day == 3:
                    if i % 10 == 0:
                        await consult_bot.send_message(consultant.chat_id, f"`{send_table}`",
                                                       parse_mode=ParseMode.MARKDOWN)
                        send_table.clear_rows()
                    try:
                        await send_birthday_message_to_client(bot=client_bot,
                                                              consultant_chat_id=consultant.chat_id,
                                                              client_chat_id=client.chat_id,
                                                              name=client.name,
                                                              text=consultant.birthday_message)
                    except aiogram.exceptions.TelegramBadRequest:
                        send_table.add_row([client.name,
                                            str(date_birth_day) + " " + date_to_month(date_birth_month) + " ❌" + "\n"])
                        i += 1
                        continue
                    send_table.add_row([client.name,
                                        str(date_birth_day) + " " + date_to_month(date_birth_month) + " ✅" + "\n"])
                    i += 1

            for client in failed:
                date_birth_month = client.date.month
                date_birth_day = client.date.day
                today_month = date.today().month
                today_day = date.today().day
                if today_month == date_birth_month and date_birth_day - today_day == 3:
                    if i % 10 == 0:
                        await consult_bot.send_message(consultant.chat_id, f"`{send_table}`",
                                                       parse_mode=ParseMode.MARKDOWN)
                        send_table.clear_rows()
                    send_table.add_row([client.name, str(date_birth_day) + " " + date_to_month(date_birth_month) + " ❌" + "\n"])
                    i += 1

        if len(send_table.rows) == 0:
            await consult_bot.send_message(consultant.chat_id, "В ближайшие 3 дня ни у кого нет дня рождения.\n "
                                                               "Список рассылки пуст")
        else:
            await consult_bot.send_message(consultant.chat_id, "Рассылка совершена:")
            await consult_bot.send_message(consultant.chat_id, f"`{send_table}`",
                                           parse_mode=ParseMode.MARKDOWN)
        await consult_bot.send_message(consultant.chat_id, "Что вы хотите сделать?",
                                       reply_markup=main_menu_keyboard())



