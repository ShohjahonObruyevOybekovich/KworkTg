import datetime

from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery
from sqlalchemy import select, insert, update, delete

from bot.buttons.inline import prog_lang_ikm, accept_denied_btn, del_edit_btn, ruyxat_order_btn
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
        product = select( Product.id,Product.title,Product.description, Product.price, ProgLang.name, Product.status).join(ProgLang).where(Product.user_id == msg.from_user.id)
        data_user = session.execute(product).fetchall()
        await msg.answer(text=data[lang]['orders_inline'])
        await state.set_state(ProductState.zakaz_state)
        for i in data_user:
            await msg.answer(text= f"#{i.id} id lik zakaz nomi👇" ,reply_markup=ruyxat_order_btn(title=i.title))

        @dp.callback_query(ProductState.zakaz_state)
        async def zakas_state_handler(call: CallbackQuery, state: FSMContext):
            data = await state.get_data()
            data['zakas_state'] = call.data
            product = select(Product.id, Product.title, Product.description, Product.price, ProgLang.name,
                             Product.status).join(ProgLang).where(Product.title == call.data)
            data_user = session.execute(product).fetchone()
            format1 = proekt_2_format.format(data_user.title, data_user.description, data_user.price, data_user.name, data_user.status)
            ic(format1)
            await msg.answer(text=format1, reply_markup=del_edit_btn(lang))

        @dp.callback_query(lambda call: call.data == data[lang]["delete_order"])
        async def delete_order(call: CallbackQuery, state: FSMContext):
            query = delete(Product).where(Product.user_id == call.from_user.id)
            session.execute(query)
            session.commit()
            await call.message.answer(text='deleted', reply_markup=customer_menu(lang))

        @dp.callback_query(lambda call: call.data == data[lang]["edit_order"])
        async def delete_order(call: CallbackQuery, state: FSMContext):
            query = delete(Product).where(Product.user_id == call.from_user.id)
            session.execute(query)
            session.commit()
            await call.message.answer(text='deleted', reply_markup=customer_menu(lang))



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
async def description_handler(call : CallbackQuery , state: FSMContext):
    data_title = await state.get_data()
    data_title['title'] = call.data
    ic(call.data)
    lang = data_title.get("lang")
    if data_title['enum'] == "accept":
        query1 = update(Product).values(status  = "ACCEPTED").where(Product.title == call.data)
        session.execute(query1)
        session.commit()
        query2 = select(Product.user_id).where(Product.title == call.data)
        chat_id = session.execute(query2)
        await call.bot.send_message(chat_id=chat_id, text=data[lang]["ACCEPT"])

    elif data_title['enum'] == "deny":

        data_title = ProductState.title()
        data_title['title'] = call.data
        lang = data_title.get("lang")
        query2 = select(Product.user_id).where(Product.title == call.data)
        chat_id = session.execute(query2)
        query1 = delete(Product).where(Product.title ==call.data)
        session.execute(query1)
        session.commit()
        await call.bot.send_message(chat_id=chat_id, text=data[lang]["DENIED"])










