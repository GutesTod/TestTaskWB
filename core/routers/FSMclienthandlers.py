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
    async with session.get(
        f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={data['articul']}"
    ) as resp:
        print(resp.text())
        await msg.answer(text=resp.text())
    await session.close()
                
    