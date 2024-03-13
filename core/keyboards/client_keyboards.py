from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder


async def menu_keyboard_factory(bool_not: bool) -> ReplyKeyboardBuilder:
    menu_kb_builder = ReplyKeyboardBuilder()
    if bool_not:
        not_text = "Отключить уведомления"
    else:
        not_text = "Включить уведомления"
    btns = [
        types.KeyboardButton(text="Получить информацию по товару"),
        types.KeyboardButton(text=not_text),
        types.KeyboardButton(text="Получить информацию из БД")
    ]
    for btn in btns:
        menu_kb_builder.row(btn)
    return menu_kb_builder