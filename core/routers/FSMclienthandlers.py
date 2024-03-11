from aiohttp import ClientSession
from aiogram import F, types, Router
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

class ImportIDState(StatesGroup):
    articul = State()
    
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
            "name": tmp_data["name"],
            "stocks": stocks
        })
    print(responce_data)
    for tmp_data in responce_data:
        printer = f'Название товара - {tmp_data['name']}\n\n'
        for stock in tmp_data['stocks']:
            printer += f"ID Склада - {stock['wh']} : Количество - {stock['qty']}\n"
        
    await msg.answer(text=printer)