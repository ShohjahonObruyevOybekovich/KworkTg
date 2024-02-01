from aiogram.fsm.state import StatesGroup, State


class UserState(StatesGroup):
    change_lang = State()
    prog_lang = State()
    lang = State()
    phone = State()

class CustomerState(StatesGroup):
    customer_menu = State()

class ProductState(StatesGroup):
    title = State()
    description = State()
    prog_lang = State()
    price = State()
    enum = State()
    zakaz_state = State()




