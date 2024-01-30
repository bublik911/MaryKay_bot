from aiogram.types import Message

from DataBase.models.ClientModel import Consultant
from DataBase.utils import connect


@connect
def get_consultant_id_by_chat_id(chat_id: int) -> int:
    return Consultant.select(Consultant.id).where(Consultant.chat_id == chat_id).get()


@connect
def count_consultants_by_phone(phone: str) -> int:
    return Consultant.select().where(Consultant.phone == phone).count()


@connect
def update_consultant_chat_id_by_phone(chat_id: int, phone: str):
    Consultant.update(chat_id=chat_id).where(Consultant.phone == phone).execute()

