from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from marshmallow import Schema, fields

from core.models.base import Base


class SecurityPrice(Base):
    __tablename__ = 'security_prices'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(8), nullable=False)
    high = Column(Float)
    low = Column(Float)
    open = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    u_high = Column(Float)
    u_low = Column(Float)
    u_open = Column(Float)
    u_close = Column(Float)
    u_volume = Column(Integer)
    date = Column(DateTime)
    change = Column(Float)
    change_percent = Column(Float)
    change_over_time = Column(Float)
    market_change_over_time = Column(Float)
    resolution = Column(String(32), nullable=False)
    timestamp = Column(DateTime)


class SecurityPriceSchema(Schema):
    id = fields.Int()
    symbol = fields.Str()
    high = fields.Float()
    low = fields.Float()
    open = fields.Float()
    close = fields.Float()
    volume = fields.Float()
    u_high = fields.Float()
    u_low = fields.Float()
    u_open = fields.Float()
    u_close = fields.Float()
    u_volume = fields.Float()
    date = fields.DateTime()
    change = fields.Float()
    change_percent = fields.Float()
    change_over_time = fields.Float()
    resolution = fields.Str()
    timestamp = fields.DateTime()
