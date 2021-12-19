from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields

from core.models.base import Base


class IexBlacklist(Base):
    __tablename__ = 'iex_blacklists'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(265), nullable=False)
    timestamp = Column(DateTime)

class IexBlacklistSchema(Schema):
    id = fields.Int()
    symbol = fields.Str()
    timestamp = fields.DateTime()