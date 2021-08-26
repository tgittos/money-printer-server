from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from core.models.base import Base


class PlaidItem(Base):
    __tablename__ = 'plaid_items'

    id = Column(Integer, primary_key=True)
    item_id = Column(String(64))
    access_token = Column(String(64))
    request_id = Column(String(32))
    timestamp = Column(DateTime)