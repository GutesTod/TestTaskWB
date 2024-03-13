from aiogram import Router, types, F
from core.keyboards import menu_keyboard_factory
from core.database.orm_query_user import add_user, get_user, switch_mode_notification
from core.database.orm_query_joins import get_articuls_of_user
from sqlalchemy.ext.asyncio import AsyncSession

client_router = Router()

@client_router.message(
    F.text == '/start'
)
async def start_bot(msg: types.Message, session: AsyncSession):
    menu_keyboard = (await menu_keyboard_factory(bool_not=True)).as_markup()
    if not (await get_user(session, msg.from_user.id)):
        await add_user(session, msg.from_user.id)
        await msg.answer(text="Новый!")
    await msg.answer(text="Привет!", reply_markup=menu_keyboard)
    
@client_router.message(
    F.text == 'Остановить уведомления'
)
async def stop_notifications(msg: types.Message, session: AsyncSession):
    switch_mode_notification(session, False, msg.from_user.id)
    await msg.answer(text="Уведомления остановлены", reply_markup=(await menu_keyboard_factory(bool_not=False)).as_markup())

@client_router.message(
    F.text == 'Включить уведомления'
)
async def on_notifications(msg: types.Message, session: AsyncSession):
    switch_mode_notification(session, True, msg.from_user.id)
    await msg.answer(text="Уведомления включены", reply_markup=(await menu_keyboard_factory(bool_not=True)).as_markup())
    
@client_router.message(
    F.text == "Получить информацию из БД"
)
async def get_info_from_db(msg: types.Message, session: AsyncSession):
    resp_data = await get_articuls_of_user(session=session, tmp_id=msg.from_user.id)
    for tmp_data in resp_data:
        printer = f'Артикул товара - {tmp_data[0].articul}\n\n'
        for stock in tmp_data:
            printer += f"ID Склада - {stock.wh_id} : Количество - {stock.qty}\n"
        await msg.answer(text=printer)