import os
import asyncio
import logging
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv

load_dotenv()

loop = asyncio.new_event_loop()
bot = Bot(token=os.getenv('API_BOT'))
dp = Dispatcher()

async def main_telegram():
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(levelname)s - %(name)s - %(message)s"
    )
    await dp.start_polling(bot)
if __name__ == '__main__':
    asyncio.run(main_telegram())