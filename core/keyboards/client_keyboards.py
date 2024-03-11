from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def menu_keyboard_factory() -> ReplyKeyboardBuilder:
    menu_kb_builder = ReplyKeyboardBuilder()
    btns = [
        types.KeyboardButton(text="Получить информацию по товару"),
        types.KeyboardButton(text="Остановить уведломления"),
        types.KeyboardButton(text="Получить информацию из БД")
    ]
    for btn in btns:
        menu_kb_builder.row(btn)
    return menu_kb_builder