from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from sqlalchemy import select

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
