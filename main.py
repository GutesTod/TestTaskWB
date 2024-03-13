import os
import sys
import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from core.routers import fsm_client_router, client_router
from core.database import async_init_db, AsyncSessionMaker, async_drop_db
from core.middleware.db import DataBaseSession


load_dotenv()

loop = asyncio.new_event_loop()
bot = Bot(token=os.getenv('API_BOT'))
dp = Dispatcher()


async def main_telegram():
    await async_drop_db()
    await async_init_db()
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    dp.include_routers(
        fsm_client_router,
        client_router
    )
    dp.update.middleware(DataBaseSession(session_pool=AsyncSessionMaker))
    await dp.start_polling(bot)
if __name__ == '__main__':
    
    if sys.platform == "win32":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    
    asyncio.run(main_telegram())