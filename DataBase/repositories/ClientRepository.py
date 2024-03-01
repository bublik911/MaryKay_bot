import datetime

from aiogram.fsm.context import FSMContext

from DataBase.models.ClientModel import Client
from DataBase.utils import connect

from typing import NoReturn


@connect
async def create_client(state: FSMContext, pid: int) -> bool:
    client = await state.get_data()
    if count_clients_by_phone(client['phone']) > 0:
        await state.clear()
        return False
    else:
        Client.create(pid=pid,
                      name=client['name'],
                      phone=client['phone'],
                      date=datetime.date(1980, client['month'], int(client['day'])))
        await state.clear()
        return True


@connect
def delete_client(phone: str, pid: int) -> int:
    return Client.update(deleted_at=datetime.date.today()).where((Client.phone == phone) &
                                                                (Client.deleted_at.is_null()) &
                                                 (Client.pid == pid)).execute()


@connect
def count_clients_by_phone(phone: str) -> int:
    return Client.select().where((Client.phone == phone) & (Client.deleted_at.is_null())).count()


@connect
def update_client_chat_id_by_phone(chat_id: int, phone: str):
    Client.update(chat_id=chat_id).where(Client.phone == phone).execute()


@connect
def get_clients_list_by_pid(pid: int) -> list:
    clients = Client.select().where((Client.pid == pid) & (Client.deleted_at.is_null()))
    return clients


@connect
def get_clients_list_by_pid_chat_id(pid: int, null_chat_id: bool) -> list:
    return Client.select().where((Client.pid == pid) &
                                    (Client.deleted_at.is_null()) &
                                    (Client.chat_id.is_null(null_chat_id)))


@connect
def get_id_by_phone_number_and_pid(phone_number: str, pid: int) -> int:
    return Client.get((Client.phone == phone_number[-10:]) & (Client.pid == pid)).id


@connect
def delete_by_id(id: int) -> NoReturn:
    today = datetime.date.today()
    Client.update(deleted_at=today).where(Client.id == id).execute()

