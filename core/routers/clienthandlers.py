from aiogram import Router, types, F

from core.keyboards import menu_keyboard_factory

client_router = Router()

@client_router.message(
    F.text == '/start'
)
async def start_bot(msg: types.Message):
    menu_keyboard = (await menu_keyboard_factory()).as_markup()
    await msg.answer(text="Привет!", reply_markup=menu_keyboard)
    
#https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={articul}