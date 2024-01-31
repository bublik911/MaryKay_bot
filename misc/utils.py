from datetime import date

from aiogram import Bot
from aiogram.types import Message

from misc.consts import months, response_months, days_in_month

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


def create_send_list(message: Message) -> list:
    pid = ConsultantRepository.get_consultant_id_by_chat_id(message.chat.id)
    clients = ClientRepository.get_clients_list_by_pid_chat_id(pid)
    response = []
    for client in clients:
        response.append([client.chat_id, client.name])
    return response


async def birthday_sending(bot: Bot):
    consultants = ConsultantRepository.get_id_chat_id_birthday_message()
    for consultant in consultants:
        clients = ClientRepository.get_clients_list_by_pid_chat_id(consultant.id)

        for client in clients:
            date_birth_month = client.date.month
            date_birth_day = client.date.day
            today_month = date.today().month
            today_day = date.today().day

            if today_month == date_birth_month and date_birth_day - today_day == 3:
                await bot.send_message(client.chat_id, f"{client.name}!")
                await bot.send_message(client.chat_id, consultant.birthday_message)
                await bot.send_message(consultant.chat_id, f"Поздравление с днем рождения послано \n{client.name}\n"
                                                           f"+7{client.phone}")
