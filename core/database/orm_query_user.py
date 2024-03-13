from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import User

async def add_user(session: AsyncSession, tmp_id: int):
    obj = User(
        id = tmp_id,
        notifications = False
    )
    session.add(obj)
    await session.commit()
    
async def get_users(session: AsyncSession):
    query = select(User)
    result = await session.execute(query)
    return result.scalars().all()

async def get_user(session: AsyncSession, tmp_id: int):
    query = select(User).where(User.id == tmp_id)
    result = await session.execute(query)
    return result.scalar()

async def switch_mode_notification(session: AsyncSession, notification_tmp: bool, tmp_id: int):
    query = update(User).where(User.id == tmp_id).values(
        notification = notification_tmp
    )
    await session.execute(query)
    await session.commit()
    