from aiogram import Router, types

from core.keyboards import menu_keyboard_factory

client_router = Router()

@client_router.message('start')
async def start_bot(msg: types.Message):
    await msg.answer(text="Привет!", reply_markup=menu_keyboard_factory())
    
#https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={articul}