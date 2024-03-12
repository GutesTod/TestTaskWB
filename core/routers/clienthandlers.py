from aiogram import Router, types, F
from core.database import get_db
from core.database.models import User, Product, Stock
from core.keyboards import menu_keyboard_factory
from sqlalchemy.orm import Session
from sqlalchemy import select

client_router = Router()

@client_router.message(
    F.text == '/start'
)
async def start_bot(msg: types.Message, session: Session = get_db()):
    menu_keyboard = (await menu_keyboard_factory(bool_not=True)).as_markup()
    if not (session.query(User).get(msg.from_user.id)):
        user_on = User(
            id = msg.from_user.id,
            notifications = True
        )
    session.add(user_on)
    await msg.answer(text="Привет!", reply_markup=menu_keyboard)
    session.close()
    
@client_router.message(
    F.text == 'Остановить уведомления'
)
async def stop_notifications(msg: types.Message, session: Session = get_db()):
    session.query(User).filter(User.id == msg.from_user.id).update({'notifications': False})
    await msg.answer(text="Уведомления остановлены", reply_markup=(await menu_keyboard_factory(bool_not=False)).as_markup())
    session.close()

@client_router.message(
    F.text == 'Включить уведомления'
)
async def on_notifications(msg: types.Message, session: Session = get_db()):
    session.query(User).filter(User.id == msg.from_user.id).update({'notifications': True})
    await msg.answer(text="Уведомления включены", reply_markup=(await menu_keyboard_factory(bool_not=True)).as_markup())
    session.close()
    
@client_router.message(
    F.text == "Получить информацию из БД"
)
async def get_info_from_db(msg: types.Message, session: Session = get_db()):
    tmp_data = session.execute(
        select(Product.articul)
        .where(Product.user_id == msg.from_user.id)
    )
    resp_data = {}
    for articul in tmp_data:
        resp_data[f'{articul}'].append(
            session.query(Stock)
            .filter(Stock.articul == articul)
            .limit(5)
            .all()
        )
    print(resp_data)
    session.close()