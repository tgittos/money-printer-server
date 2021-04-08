from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float

Base = declarative_base()

class Sync(Base):
    __tablename__ = 'sync'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(10))
    last_update = Column(DateTime)