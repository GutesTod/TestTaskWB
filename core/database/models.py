import os
from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from sqlalchemy.orm import relationship, DeclarativeBase
from sqlalchemy.ext.asyncio import AsyncAttrs, create_async_engine, async_sessionmaker, AsyncSession

from dotenv import load_dotenv

load_dotenv()

engine = create_async_engine(
  os.getenv("DATABASE_URL")
)

engine.connect()

AsyncSessionMaker = async_sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


class Base(AsyncAttrs, DeclarativeBase):
  pass

class User(Base):
  __tablename__ = "users"

  id = Column(Integer, primary_key=True)
  notifications = Column(Boolean)


class Product(Base):
  __tablename__ = "products"

  articul = Column(Integer, primary_key=True, autoincrement=True)
  user_id = Column(Integer, ForeignKey("users.id"))
  name_product = Column(String)

  user = relationship("User", backref="products")

class Stock(Base):
  __tablename__ = "stocks"

  id = Column(Integer, autoincrement=True, primary_key=True)
  articul = Column(Integer, ForeignKey("products.articul"))
  wh_id = Column(Integer)
  qty = Column(Integer)

  product = relationship("Product", backref="stocks")
  
async def async_init_db():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.create_all)
    
async def async_drop_db():
  async with engine.begin() as conn:
    await conn.run_sync(Base.metadata.drop_all) 
  