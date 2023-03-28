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