from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder

async def sub_keyboard_factory() -> InlineKeyboardBuilder:
    keyboard = InlineKeyboardBuilder()
    subBtn = types.InlineKeyboardButton(text="Подписаться на артикуль", callback_data='sub-articul')
    keyboard.row(subBtn)
    return keyboard