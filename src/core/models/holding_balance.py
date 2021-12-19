from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields

from core.models.base import Base


class HoldingBalance(Base):
    __tablename__ = 'holding_balances'

    id = Column(Integer, primary_key=True)
    holding_id = Column(Integer, ForeignKey("holdings.id"), nullable=False)
    cost_basis = Column(Float)
    quantity = Column(Float)
    timestamp = Column(DateTime)


class HoldingBalanceSchema(Schema):
    id = fields.Int()
    holding_id = fields.Int()
    cost_basis = fields.Float()
    quantity = fields.Float()
    timestamp = fields.DateTime()