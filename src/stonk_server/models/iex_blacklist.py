from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey

from .base import Base


class IexBlacklist(Base):
    __tablename__ = 'iex_blacklists'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(265), nullable=False)
    timestamp = Column(DateTime)
