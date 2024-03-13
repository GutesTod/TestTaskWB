from aiohttp import ClientSession
from aiogram import F, types, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext
from core.keyboards import sub_keyboard_factory
from sqlalchemy.ext.asyncio import AsyncSession
from core.database.orm_query_product import add_product
from core.database.orm_query_stocks import add_stock

class ImportIDState(StatesGroup):
    articul = State()
    resp_data = State()
    
fsm_client_router = Router()

@fsm_client_router.message(
    F.text == "Получить информацию по товару"
)
async def import_articul(msg: types.Message, state: FSMContext):
    await msg.answer(text="Напишите артикуль товара")
    await state.set_state(ImportIDState.articul)
    
@fsm_client_router.message(
    ImportIDState.articul
)
async def get_info_about_product(msg: types.Message, state: FSMContext):
    await state.update_data(articul=int(msg.text))
    data = await state.get_data()
    session = ClientSession()
    json_data = None
    responce_data = []
    async with session.get(
        f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={data['articul']}"
    ) as resp:
        json_data = (await resp.json())
    await session.close()
    for tmp_data in json_data['data']['products']:
        stocks = []
        for tmp_sizes in tmp_data["sizes"]:
            for tmp_stocks in tmp_sizes["stocks"]:
                print(tmp_stocks)
                stocks.append({
                    "wh": tmp_stocks['wh'],
                    "qty": tmp_stocks['qty']
                })
        responce_data.append({
            "articul": data['articul'],
            "name": tmp_data["name"],
            "stocks": stocks
        })
    await state.update_data(resp_data=responce_data)
    await state.set_state(ImportIDState.resp_data)
    for tmp_data in responce_data:
        printer = f'Название товара - {tmp_data['name']}\n\n'
        for stock in tmp_data['stocks']:
            printer += f"ID Склада - {stock['wh']} : Количество - {stock['qty']}\n"
        
    await msg.answer(text=printer, reply_markup=(await sub_keyboard_factory()).as_markup())
    
@fsm_client_router.callback_query(
    ImportIDState.resp_data,
    F.data == "sub-articul"
)
async def sub_articul(callback: types.CallbackQuery, state: FSMContext, session: AsyncSession):
    data = await state.get_data()
    for tmp_data in data['resp_data']:
        await add_product(session, callback.from_user.id, tmp_data)
        for tmp_stock in tmp_data['stocks']:
            await add_stock(session, tmp_stock, tmp_data['articul'])
    callback.message.answer(text="Вы подписались!")