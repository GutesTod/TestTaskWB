from sqlalchemy import Column, Integer, String, ForeignKey, Boolean
from core.database import Base
from sqlalchemy.orm import relationship

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

  articul = Column(Integer, ForeignKey("products.articul"), primary_key=True)
  wh_id = Column(Integer)
  qty = Column(Integer)

  product = relationship("Product", backref="stocks")