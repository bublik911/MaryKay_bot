from DataBase.config import *
from aiogram.types import Message
from datetime import date
from aiogram import Bot
from misc.consts import months, response_months


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
    db.connect(reuse_if_open=True)
    pid = Consultant.get(Consultant.chat_id == message.chat.id).id
    clients = Client.select().where((Client.pid == pid) &
                                    (Client.deleted_at.is_null()) &
                                    (Client.chat_id.is_null(False)))
    db.close()
    response = []
    for client in clients:
        response.append([client.chat_id, client.name])
    return response


async def birthday_sending(bot: Bot):
    db.connect(reuse_if_open=True)
    consultants = Consultant.select(Consultant.id, Consultant.chat_id, Consultant.birthday_message)
    for consultant in consultants:
        clients = Client.select().where((Client.pid == 1) &
                                        (Client.deleted_at.is_null()) &
                                        (Client.chat_id.is_null(False)))
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
    db.close()