from apscheduler.schedulers.asyncio import AsyncIOScheduler
from aiogram import Dispatcher
from sqlalchemy.orm import Session
from core.database import get_db


async def send_products_to_users(dp: Dispatcher, session: Session = get_db):
    ...
    
def schedule_jobs(scheduler: AsyncIOScheduler, dp: Dispatcher):
    scheduler.add_job(send_products_to_users, "interval", minutes=5, args=(dp, ))