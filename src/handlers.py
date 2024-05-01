import datetime

import aiogram.client.bot
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


router = Router()
    

# @logger.catch()
# @router.message(Command("test"))
# async def start_command_handler(message: Message):
#     logger.info(f"New order from user @{message.from_user.username}")
#     await message.answer("OK")
    
    
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
    await bot.send_message(chat_id=WORKERS_GROUP_ID, text=text.new_order.format(
        rate="\n🚨🚨🚨СРОЧНО‼️" if data["rate"] == "immediately" else "",
        username=data["username"],
        title=data["title"],
        mark=data["mark"],
        email=data["email"],
        price=data["price"],
        time=datetime.datetime.now().strftime("%d.%m.%Y %H:%M:%S"),
        comment=data["comment"],
    ))
    await callback.message.edit_text(text.order_confirmed, reply_markup=None)
