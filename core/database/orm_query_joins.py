from sqlalchemy import select, join
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import Stock
from core.database.orm_query_product import get_articuls_by_user_id

async def get_articuls_of_user(session: AsyncSession, tmp_id: int):
    tmp_data = []
    articuls = await get_articuls_by_user_id(session=session, tmp_id=tmp_id)
    for articul in articuls:
        query = select(Stock).where(Stock.articul == articul)
        data = await session.execute(query)
        tmp_data.append(data.scalars().all())
    return tmp_data