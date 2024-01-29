import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, insert

from bot.buttons.inline import prog_lang_ikm, accept_denied_btn
from bot.buttons.reply import customer_menu, menu_btn
from bot.buttons.text import product_format
from bot.enums.main import StatusEnum
from bot.lang.main import data
from bot.state.main import CustomerState, ProductState
from db.connect import session
from db.model import Customer, Product
from dispatcher import dp


@dp.message(lambda msg : msg.text in [data['uz']["customer"],data['en']["customer"]])
async def customer_handler(msg : Message , state : FSMContext):
    data = await state.get_data()
    query = select(Customer).where(Customer.user_id == msg.from_user.id)
    customer = session.execute(query).fetchone()
    if not customer:
        q = insert(Customer).values(user_id = msg.from_user.id)
        session.execute(q)
        session.commit()
    await state.set_state(CustomerState.customer_menu)
    await msg.answer("Menu" , reply_markup=customer_menu(data.get("lang")))

@dp.message(CustomerState.customer_menu)
async def customer_menu_handler(msg : Message , state : FSMContext):
    state_data = await state.get_data()
    lang = state_data.get("lang")
    if msg.text == data[lang]['order']:
        await state.set_state(ProductState.prog_lang)
        await msg.answer(text = data[lang]["prog_lang"], reply_markup=prog_lang_ikm())
    elif msg.text == data[lang]['order_history']: # TODO
        pass
    elif msg.text == data[lang]['back']:
        await msg.answer("Back" , reply_markup=menu_btn(lang))

@dp.callback_query(ProductState.prog_lang)
async def prog_lang_handler(call : CallbackQuery , state : FSMContext):
    state_data = await state.get_data()
    await call.message.delete()
    lang  = state_data.get("lang")
    prog_id = int(call.data.split("_")[1])
    state_data["prog_id"] = prog_id
    await state.set_data(state_data)
    await state.set_state(ProductState.title)
    await call.message.answer(data[lang]['title'])

@dp.message(ProductState.title)
async def title_handler(msg : Message , state : FSMContext):
    state_data = await state.get_data()
    lang = state_data.get("lang")
    state_data['title'] = msg.text
    await state.set_data(state_data)
    await state.set_state(ProductState.description)
    await msg.answer(data[lang]['description'])


@dp.message(ProductState.description)
async def description_handler(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    lang = state_data.get("lang")
    state_data['description'] = msg.text
    await state.set_data(state_data)
    await state.set_state(ProductState.price)
    await msg.answer(data[lang]['price'])


@dp.message(ProductState.price)
async def price_handler(msg: Message, state: FSMContext):
    state_data = await state.get_data()
    product = {
        "title" : state_data.get("title"),
        "description" : state_data.get("description"),
        "price" : msg.text,
        "prog_lang_id" : state_data.get("prog_id"),
        "user_id" : msg.from_user.id,
        "status" : StatusEnum.process.value,
    }
    lang = state_data.get("lang")
    session.execute(insert(Product).values(**product))
    session.commit()
    product = session.execute(select(Product).where(Product.title == product.get("title"))).fetchone()[0]
    await state.clear()
    await state.set_data({"lang" : lang})
    format = product_format.format(product.id ,  product.prog_lang.name ,product.title , product.description , product.price)
    await msg.bot.send_message(1148477816 ,text= format, reply_markup=accept_denied_btn())
    await msg.answer("Adminga Tastiqlash uchun yuborildi ⏳", reply_markup=customer_menu(lang))














