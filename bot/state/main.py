from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    change_lang = State()
    prog_lang = State()
    lang = State()
    phone = State()
