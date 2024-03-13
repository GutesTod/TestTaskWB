from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import Stock

async def add_stock(session: AsyncSession, data: dict, articul: int):
    obj = Stock(
        articul=articul,
        wh_id=data['wh'],
        qty=data['qty']
    )
    session.add(obj)
    await session.commit()
    
async def get_stocks_by_articul(session: AsyncSession, articul: int):
    query = select(Stock).where(Stock.articul == articul)
    result = await session.execute(query)
    return result.scalars().all()