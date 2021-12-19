from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields

from core.models.base import Base


class AccountBalance(Base):
    __tablename__ = 'account_balances'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    available = Column(Float)
    current = Column(Float)
    iso_currency_code = Column(String(8))
    timestamp = Column(DateTime)

class AccountBalanceSchema(Schema):
    id = fields.Int()
    account_id = fields.Int()
    available = fields.Float()
    current = fields.Float()
    iso_currency_code = fields.Str()
    timestamp = fields.DateTime()