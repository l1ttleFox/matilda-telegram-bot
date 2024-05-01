from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton, ReplyKeyboardMarkup, ReplyKeyboardRemove

start_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Оформить заказ", callback_data="make_order")],
])

mark_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="4 (800р)", callback_data="mark_4"), InlineKeyboardButton(text="5 (1200р)", callback_data="mark_5")],
])

rate_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Срочно (в течение 12 часов)", callback_data="rate_immediately")],
    [InlineKeyboardButton(text="Не срочно (в течение 3 суток)", callback_data="rate_classic")],
])

confirm_menu = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Да, все верно", callback_data="confirmed")],
    [InlineKeyboardButton(text="Нет, все сначала", callback_data="make_order")],
])
