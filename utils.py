from DataBase.models_db import *
from aiogram.types import Message
months = ["Январь", "Февраль", "Март", "Апрель", "Май", "Июнь", "Июль", "Август", "Сентябрь", "Октябрь", "Ноябрь", "Декабрь"]


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


def create_clients_list(message: Message) -> list:
    pid = Consultant.get(Consultant.chat_id == message.chat.id).id
    clients = Client.select().where((Client.pid == pid) & (Client.deleted_at.is_null()))
    response = []
    k = 0
    for client in clients:
        k += 1
        month, day = str(client.date).split("-")[1:]
        response.append(f"{k} {client.name} {month}-{day}\n"
                        f" +7{client.phone}")
    return response
