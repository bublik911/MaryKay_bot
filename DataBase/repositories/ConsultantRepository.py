from aiogram.types import Message

from typing import NoReturn

from DataBase.models.ClientModel import Consultant
from DataBase.utils import connect


@connect
def get_consultant_id_by_chat_id(chat_id: int) -> int:
    return Consultant.select(Consultant.id).where(Consultant.chat_id == chat_id).get()


@connect
def get_all_message(message: Message) -> str:
    return Consultant.get(Consultant.chat_id == message.chat.id).all_message


@connect
def get_birthday_message(message: Message) -> str:
    return Consultant.get(Consultant.chat_id == message.chat.id).birthday_message


@connect
def get_id_chat_id_birthday_message() -> list:
    return Consultant.select(Consultant.id, Consultant.chat_id, Consultant.birthday_message)


@connect
def count_consultants_by_phone(phone: str) -> int:
    return Consultant.select().where(Consultant.phone == phone).count()


@connect
def update_consultant_chat_id_by_phone(chat_id: int, phone: str):
    Consultant.update(chat_id=chat_id).where(Consultant.phone == phone).execute()


@connect
def update_all_message(message: Message) -> NoReturn:
    Consultant.update(all_message=message.text).where(Consultant.chat_id == message.chat.id).execute()


@connect
def update_birthday_message(message: Message) -> NoReturn:
    Consultant.update(birthday_message=message.text).where(Consultant.chat_id == message.chat.id).execute()
