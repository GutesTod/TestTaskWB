from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from core.database.models import Product

async def add_product(session: AsyncSession, tmp_id: int, data: dict):
    obj = Product(
        articul=data['articul'],
        user_id=tmp_id,
        name_product=data['name']
    )
    session.add(obj)
    await session.commit()
    
async def get_products_by_user_id(session: AsyncSession, tmp_id: int):
    query = select(Product).where(Product.user_id == tmp_id)
    result = await session.execute(query)
    return result.scalars().all()

async def get_articuls_by_user_id(session: AsyncSession, tmp_id: int):
    query = select(Product.articul).where(Product.user_id == tmp_id)
    result = await session.execute(query)
    return result.scalars().all()