import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, insert, update, delete

from bot.buttons.inline import prog_lang_ikm, accept_denied_btn, del_edit_btn
from bot.buttons.reply import customer_menu, menu_btn
from bot.buttons.text import product_format, proekt_2_format
from bot.enums.main import StatusEnum
from bot.lang.main import data
from bot.state.main import CustomerState, ProductState
from db.connect import session
from db.model import Customer, Product, ProgLang
from dispatcher import dp
from icecream import ic


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
    elif msg.text == data[lang]['order_history']:
        product = select( Product.title,Product.description, Product.price, ProgLang.name, Product.status).join(ProgLang).where(Product.user_id == msg.from_user.id)
        data_user = session.execute(product).fetchall()
        for i in data_user:
            format1 = proekt_2_format.format(i.title, i.description, i.price, i.name, i.status)
            ic(format1)
            await msg.answer(text=format1, reply_markup=del_edit_btn(lang))

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
    await state.set_data({"lang" : lang})
    format = product_format.format(product.id ,  product.prog_lang.name ,product.title , product.description , product.price)

    try:
        await msg.bot.send_message(5995495508 ,text= format, reply_markup=accept_denied_btn())
        await state.set_state(ProductState.enum)
    except:
        await msg.answer(text='Bot bu yunalish buyicha freelanser topolmadi ')
    await msg.answer(text=data[lang]["send_to_admin"],reply_markup=customer_menu(lang))


# Xato callback bulish kk
@dp.callback_query(ProductState.enum)
async def description_handler(msg: Message, state: FSMContext):
    data_title = await state.get_data()
    data_title['title'] = msg.text
    ic(msg.text)
    lang = data_title.get("lang")
    if data_title['enum'] == "accept":
        query1 = update(Product).values(status  = "ACCEPTED").where(Product.title == msg.text)
        session.execute(query1)
        session.commit()
        query2 = select(Product.user_id).where(Product.title == msg.text)
        chat_id = session.execute(query2)
        await msg.bot.send_message(chat_id=chat_id, text=data[lang]["ACCEPT"])

    elif data_title['enum'] == "deny":
        data_title = ProductState.title()
        data_title['title'] = msg.text
        lang = data_title.get("lang")
        query2 = select(Product.user_id).where(Product.title == msg.text)
        chat_id = session.execute(query2)
        query1 = delete(Product).where(Product.title ==msg.text)
        session.execute(query1)
        session.commit()
        await msg.bot.send_message(chat_id=chat_id, text=data[lang]["DENIED"])













