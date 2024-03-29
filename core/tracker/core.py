from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Bot
from aiohttp import ClientSession
from core.database import AsyncSessionMaker
from core.database.orm_query_product import get_all_products
from core.database.orm_query_stocks import update_stocks
from core.database.orm_query_user import get_user


async def send_products_to_users(bot: Bot):
    print("Тест")
    async with AsyncSessionMaker() as session:
        data = await get_all_products(session=session)
        for tmp in data:
            sessionhttp = ClientSession()
            json_data = None
            responce_data = []
            async with sessionhttp.get(
                f"https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm={tmp.articul}"
            ) as resp:
                json_data = (await resp.json())
            await sessionhttp.close()
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
                    "articul": tmp.articul,
                    "name": tmp_data["name"],
                    "stocks": stocks
                })
            for tmp_data in responce_data:
                printer = f'Название товара - {tmp_data['name']}\n\n'
                for stock in tmp_data['stocks']:
                    printer += f"ID Склада - {stock['wh']} : Количество - {stock['qty']}\n"
                    await update_stocks(session, tmp_data['articul'], stock['wh'], stock['qty'])
            data_user = await get_user(session, tmp.user_id)
            if data_user.notifications == True:
                await bot.send_message(chat_id=tmp.user_id, text=printer)