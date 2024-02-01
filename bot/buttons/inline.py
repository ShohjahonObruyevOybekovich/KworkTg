from itertools import chain

from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import select
from aiogram.utils.keyboard import InlineKeyboardBuilder
from bot.lang.main import data
from db.connect import session
from db.model import ProgLang


def language_ibtn():
    uz_btn = InlineKeyboardButton(text="Uzbek 🇺🇿", callback_data="uz")
    en_btn = InlineKeyboardButton(text="English 🏴󠁧󠁢󠁥󠁮󠁧󠁿", callback_data="en")
    return InlineKeyboardMarkup(inline_keyboard=[[uz_btn , en_btn]])

def prog_lang_ikm():
    prog_langs: list[tuple] = session.execute(select(ProgLang)).fetchall()
    design = []
    row = []
    for i in prog_langs:
        row.append(InlineKeyboardButton(text = i[0].name , callback_data=f"prog_{i[0].id}"))
        if len(row) == 2:
            design.append(row)
            row = []
    if row:
        design.append(row)
    return InlineKeyboardMarkup(inline_keyboard=design)

def accept_denied_btn():
    deny_btn = InlineKeyboardButton(text="🔴 DENY", callback_data="deny")
    accept_btn = InlineKeyboardButton(text="🟢 ACCEPT", callback_data="accept")
    return InlineKeyboardMarkup(inline_keyboard=[[deny_btn, accept_btn]])

def del_edit_btn(lang):
    del_btn = InlineKeyboardButton(text=data[lang]['delete_order'], callback_data='deleting_order')
    edit_btn = InlineKeyboardButton(text=data[lang]['edit_order'], callback_data='editing_order')
    return InlineKeyboardMarkup(inline_keyboard=[[del_btn,edit_btn]])

def ruyxat_order_btn(title):
    keyboard = InlineKeyboardBuilder()

    buttons = [
        [title]
    ]
    keyboard.row(*[InlineKeyboardButton(text=i, callback_data=i) for i in chain(*buttons)], width=1)
    # post_page += 1
    return keyboard.as_markup()
