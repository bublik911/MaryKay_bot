from aiogram.fsm.state import StatesGroup, State


class Start(StatesGroup):
    client = State()
    consultant = State()


class CheckBase(StatesGroup):
    start = State()
    ok = State()
    delete = State()
    check = State()


class AddClient(StatesGroup):
    name = State()
    phone = State()
    month = State()
    day = State()
    finish = State()
    commit = State()


class Sending(StatesGroup):
    choose = State()
    all = State()
    all_edit_start = State()
    all_edited = State()
    birthday = State()
    birthday_edit_start = State()
    birthday_edited = State()
