from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def menu_keyboard_factory(bool_not: bool) -> ReplyKeyboardBuilder:
    menu_kb_builder = ReplyKeyboardBuilder()
    btns = [
        types.KeyboardButton(text="Получить информацию по товару"),
        types.KeyboardButton(text=("Включить уведомления" if bool_not else "Отключить уведомления")),
        types.KeyboardButton(text="Получить информацию из БД")
    ]
    for btn in btns:
        menu_kb_builder.row(btn)
    return menu_kb_builder