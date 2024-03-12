import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from core.routers import fsm_client_router, client_router
from sqlalchemy_utils import database_exists, create_database
from core.database import engine


load_dotenv()

loop = asyncio.new_event_loop()
bot = Bot(token=os.getenv('API_BOT'))
dp = Dispatcher()

async def on_startup():
    if not database_exists(engine.url):
        create_database(engine.url)

async def main_telegram():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    dp.include_routers(
        fsm_client_router,
        client_router
    )
    await dp.start_polling(bot, on_startup=on_startup)
if __name__ == '__main__':
    asyncio.run(main_telegram())