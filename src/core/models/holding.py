from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields

from core.models.base import Base


class Holding(Base):
    __tablename__ = 'holdings'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    security_id = Column(Integer, ForeignKey("securities.id"), nullable=False)
    cost_basis = Column(Float)
    quantity = Column(Float)
    iso_currency_code = Column(String(8))
    timestamp = Column(DateTime)


class HoldingSchema(Schema):
    id = fields.Int()
    account_id = fields.Int()
    security_id = fields.Int()
    cost_basis = fields.Float()
    quantity = fields.Float()
    iso_currency_code = fields.Str()
    timestamp = fields.DateTime()