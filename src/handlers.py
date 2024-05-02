import datetime

from loguru import logger
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext

from loader import bot
import keyboard as kb
import text
from config import WORKERS_GROUP_ID
from states import MakingOrder
from db import session, Order


router = Router()
    

@logger.catch()
@router.message(Command("test"))
async def start_command_handler(message: Message):
    logger.info(f"New order from user @{message.from_user.username}")
    await message.answer("OK")
    
    
@logger.catch()
@router.message(Command("order"))
@router.message(Command("start"))
async def start_command_handler(message: Message):
    logger.info(f"New order from user @{message.from_user.username}")
    await message.answer(text.welcome.format(name=message.from_user.full_name), reply_markup=kb.start_menu)
    
    
@logger.catch()
@router.callback_query(F.data == "make_order")
async def make_order_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.set_state(MakingOrder.title)
    await callback.message.edit_text(text.get_title)
    

@logger.catch()
@router.message(MakingOrder.title)
async def get_project_title(message: Message, state: FSMContext) -> None:
    await state.update_data(title=message.text)
    await state.update_data(username=message.from_user.username)
    await state.set_state(MakingOrder.mark)
    await message.answer(text.get_mark, reply_markup=kb.mark_menu)
    

@logger.catch()
@router.callback_query(F.data.startswith("mark_"))
async def mark_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(mark=callback.data[5:])
    await state.set_state(MakingOrder.rate)
    await callback.message.edit_text(text.get_rate, reply_markup=kb.rate_menu)


@logger.catch()
@router.callback_query(F.data.startswith("rate_"))
async def rate_callback(callback: CallbackQuery, state: FSMContext) -> None:
    await state.update_data(rate=callback.data[5:])
    await state.set_state(MakingOrder.comment)
    await callback.message.edit_text(text.get_comment, reply_markup=None)

    
@logger.catch()
@router.message(MakingOrder.comment)
async def get_comment(message: Message, state: FSMContext) -> None:
    await state.update_data(comment=message.text)
    await state.set_state(MakingOrder.email)
    await message.answer(text.get_email, reply_markup=None)
    
    
@logger.catch()
@router.message(MakingOrder.email)
async def get_user_email(message: Message, state: FSMContext) -> None:
    await state.update_data(email=message.text)
    await state.set_state(MakingOrder.confirm)
    
    data = await state.get_data()
    data["price"] = 800 if data["mark"] == "4" else 1200
    if data["rate"] == "immediately":
        data["price"] = data["price"] * 1.4
    confirm_text = text.confirm.format(
        title=data["title"],
        mark=data["mark"],
        rate="✅" if data["rate"] == "immediately" else "⛔️",
        comment=data["comment"],
        email=data["email"],
        price=data["price"],
    )
    await message.answer(confirm_text, reply_markup=kb.confirm_menu)
    
    
@logger.catch()
@router.callback_query(F.data == "confirmed")
async def confirm_order(callback: CallbackQuery, state: FSMContext) -> None:
    data = await state.get_data()
    data["price"] = 800 if data["mark"] == "4" else 1200
    if data["rate"] == "immediately":
        data["price"] = data["price"] * 1.4
    dt = datetime.datetime.now() + datetime.timedelta(hours=3)
    message = await bot.send_message(chat_id=WORKERS_GROUP_ID, text=text.new_order.format(
        rate="\n🚨🚨🚨СРОЧНО‼️" if data["rate"] == "immediately" else "",
        username=data["username"],
        title=data["title"],
        mark=data["mark"],
        email=data["email"],
        price=data["price"],
        time=dt.strftime("%d.%m.%Y %H:%M:%S"),
        comment=data["comment"],
    ))
    await bot.pin_chat_message(chat_id=WORKERS_GROUP_ID, message_id=message.message_id)
    await callback.message.edit_text(text.order_confirmed, reply_markup=None)
    await state.clear()
    
    order = Order(
        customer_username=data["username"],
        title=data["title"],
        mark=int(data["mark"]),
        immediately=True if data["rate"] == "immediately" else False,
        price=int(data["price"]),
        email=data["email"],
        message_id=message.message_id,
        comment=data["comment"]
    )
    session.add(order)
    session.commit()


@logger.catch()
@router.message(lambda m: m.chat.id == WORKERS_GROUP_ID and m.text == "ГОТОВО")
async def order_done(message: Message):
    if message.reply_to_message:
        if message.reply_to_message.message_id in session.query(Order.message_id).filter(Order.released is False).all():
            bot.unpin_chat_message(WORKERS_GROUP_ID, message.reply_to_message.message_id)
            order = session.query(Order).filter(Order.message_id == message.reply_to_message.message_id).one()
            order.released = True
            order.release_date = datetime.datetime.now()
            session.commit()
            
            await message.answer("Отлично! Отметил заказ выполненным. Можете переходить к следующим.")
            
            
@logger.catch()
@router.message(Command("orders"))
async def show_all_orders(message: Message) -> None:
    if message.chat.id == WORKERS_GROUP_ID:
        result = ""
        for i_order in session.query(Order).all():
            result += f"заказ #{i_order.id} \t| {'выполнен' if i_order.released else 'в процессе'}\t| на {i_order.mark}\t| {'срочно' if i_order.immediately else 'не срочно'} {i_order.customer_username}\n"
            
        await message.answer(result)
        
        
@logger.catch()
@router.message(lambda m: m.text.startswith("/order "))
async def show_detail_order(message: Message):
    try:
        order_id = int(message.text.split()[1])
        order = session.query(Order).filter(Order.id == order_id).one()
        result = text.show_detail_order.format(
            id=order.id,
            username=order.customer_username,
            title=order.title,
            mark=order.mark,
            immediately="да" if order.immediately else "нет",
            price=order.price,
            email=order.email,
            comment=order.comment,
            confirma_date=order.confirm_date,
            status="выполнен" if order.released else "в процессе",
            released_date=order.release_date if order.released else ""
        )
        await message.answer(result)
        
    except:
        await message.answer("Неверный формат команды. /order <order_id>")