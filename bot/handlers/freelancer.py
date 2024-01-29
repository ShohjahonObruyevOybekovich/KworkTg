import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import update, insert

from bot.buttons.inline import prog_lang_ikm
from bot.buttons.reply import phone_number_btn, menu_btn
from bot.lang.main import data
from bot.state.main import UserState
from db.connect import session
from db.model import User, Freelancer
from dispatcher import dp


@dp.message(lambda msg : msg.text in [data['uz']["freelancer"],data['en']["freelancer"]])
async def freelancer_handler(msg : Message , state : FSMContext):
    await state.set_state(UserState.prog_lang)
    await msg.answer("Programmer lang ", reply_markup=prog_lang_ikm())


@dp.callback_query(UserState.prog_lang)
async def prog_lang_handler(call : CallbackQuery , state : FSMContext):
    await call.message.delete()
    prog_id = int(call.data.split("_")[1])
    data = await state.get_data()
    data["prog_id"] = prog_id
    await state.set_data(data)
    await state.set_state(UserState.phone)
    await call.message.answer("Phone Number 👇", reply_markup=phone_number_btn(data.get('lang')))



@dp.message(UserState.phone)
async def phone_handler(msg : Message , state : FSMContext):
    phone_number = msg.contact.phone_number
    data = await state.get_data()
    query1 = update(User).values(phone=phone_number).where(User.chat_id == msg.from_user.id)
    query2 = insert(Freelancer).values(chat_id = msg.from_user.id , prog_lang_id = data['prog_id'] , join_date = datetime.datetime.now())
    session.execute(query1)
    session.execute(query2)
    session.commit()
    await msg.answer("Success Save" , reply_markup=menu_btn(data.get("lang")))