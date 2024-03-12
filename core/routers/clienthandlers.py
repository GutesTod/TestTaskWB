from aiogram import Router, types, F
from database import get_db, User
from core.keyboards import menu_keyboard_factory
from sqlalchemy.orm import Session

client_router = Router()

@client_router.message(
    F.text == '/start'
)
async def start_bot(msg: types.Message, session: Session = get_db):
    menu_keyboard = (await menu_keyboard_factory()).as_markup()
    user_on = User(
        id = msg.from_user.id
    )
    await msg.answer(text="Привет!", reply_markup=menu_keyboard)
    
