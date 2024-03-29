from aiogram.fsm.state import StatesGroup, State


class Transition(StatesGroup):
    transition = State()


class Start(Transition):
    waiting = State()


class CheckBase(Transition):
    waiting = State()


class AddClient(Transition):
    name = State()
    phone = State()
    month = State()
    day = State()
    finish = State()
    commit = State()


class DeleteClient(Transition):
    confirm = State()
    commit = State()


class Menu(Transition):
    waiting = State()


class Sending(Transition):
    choose = State()

    all = State()
    all_edit_start = State()
    all_text_edit = State()
    all_photo_edit = State()
    all_edited = State()

    birthday = State()
    birthday_edit_start = State()
    birthday_text_edit = State()
    birthday_photo_edit = State()
    birthday_edited = State()
