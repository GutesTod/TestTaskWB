import os

from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base



from dotenv import load_dotenv

load_dotenv()

engine = create_engine(
    os.getenv("DATABASE_URL")
)

Base = declarative_base()

Base.metadata.create_all(engine)

engine.connect()

SessionLocal = sessionmaker(bind=engine)

def get_db():
    db = SessionLocal()
    return db