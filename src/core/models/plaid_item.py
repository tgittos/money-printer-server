from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from core.models.base import Base


class PlaidItem(Base):
    __tablename__ = 'plaid_items'

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    item_id = Column(String(64))
    access_token = Column(String(64))
    request_id = Column(String(32))
    status = Column(String(128))
    timestamp = Column(DateTime)
