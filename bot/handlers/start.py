from datetime import datetime

from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from aiogram.utils.markdown import hbold
from sqlalchemy import insert, select, update
from sqlalchemy.sql.functions import session_user

from bot.buttons.inline import language_ibtn, prog_lang_ikm
from bot.buttons.reply import menu_btn, phone_number_btn
from bot.lang.main import data
from bot.state.main import UserState
from db.connect import session
from db.model import User
from dispatcher import dp


@dp.message(CommandStart())
async def command_start_handler(message: Message, state : FSMContext) -> None:
    query = select(User).where(User.chat_id == message.from_user.id)
    user = session.execute(query).fetchone()
    if not user:
        await state.set_state(UserState.lang)
        await message.answer(f"Hello, {hbold(message.from_user.full_name)}!")
        await message.answer(f"Tilni tanlang!" , reply_markup=language_ibtn())
    else:
        data = await state.get_data()
        data["lang"] = user[0].lang
        await state.set_data(data)
        await message.answer("Menu", reply_markup=menu_btn(user[0].lang))


@dp.callback_query(UserState.lang)
async def lang_handler(call : CallbackQuery , state : FSMContext):
    await call.message.delete()
    data = await state.get_data()
    data["lang"] = call.data
    await state.set_data(data)
    query = insert(User).values(chat_id = call.from_user.id , lang = call.data, join_date = datetime.now())
    session.execute(query)
    session.commit()
    await call.message.answer("Menu" , reply_markup=menu_btn(call.data))

@dp.message(lambda msg : msg.text in [data['uz']["change_lang"],data['en']["change_lang"]])
async def change_lang_handler(msg : Message , state : FSMContext):
    await state.set_state(UserState.change_lang)
    await msg.answer("Tilni tanlang !", reply_markup=language_ibtn())

@dp.callback_query(UserState.change_lang)
async def change_lang_handler(call : CallbackQuery , state : FSMContext):
    await call.message.delete()
    data = await state.get_data()
    data["lang"] = call.data
    await state.set_data(data)
    query = update(User).values(lang = call.data).where(User.chat_id == call.from_user.id)
    print(query)
    session.execute(query)
    session.commit()
    await call.message.answer("Change Success !" , reply_markup=menu_btn(call.data))



