from aiogram.types import KeyboardButton, ReplyKeyboardMarkup

from bot.lang.main import data



def phone_number_btn(lang):
    return ReplyKeyboardMarkup(keyboard=[[KeyboardButton(text = data[lang]["phone_number"], request_contact=True) ]] , resize_keyboard=True)
def menu_btn(lang):
    texts: dict = data[lang]
    k1 = KeyboardButton(text = texts['freelancer'])
    k2 = KeyboardButton(text = texts['customer'])
    k3 = KeyboardButton(text = texts['vacancies'])
    k4 = KeyboardButton(text = texts['change_lang'])
    design = [
        [k1 , k2],
        [k3],
        [k4]
    ]
    return ReplyKeyboardMarkup(keyboard=design , resize_keyboard=True)

def customer_menu(lang):
    texts: dict = data[lang]
    k1 = KeyboardButton(text = texts['order'])
    k2 = KeyboardButton(text = texts['order_history'])
    k3 = KeyboardButton(text = texts['back'])

    design = [
        [k1 , k2],
        [k3],
    ]
    return ReplyKeyboardMarkup(keyboard=design , resize_keyboard=True)



