from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields

from core.models.base import Base


class InvestmentTransaction(Base):
    __tablename__ = 'investment_transactions'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    name = Column(String(512))
    amount = Column(Float)
    fees = Column(Float)
    price = Column(Float)
    quantity = Column(Float)
    date = Column(DateTime)
    investment_transaction_id = Column(String(256))
    iso_currency_code = Column(String(8))
    type = Column(String(32))
    subtype = Column(String(32))
    timestamp = Column(DateTime)


class InvestmentTransactionSchema(Schema):
    id = fields.Int()
    account_id = fields.Int()
    name = fields.Str()
    amount = fields.Float()
    fees = fields.Float()
    price = fields.Float()
    quantity = fields.Float()
    date = fields.DateTime()
    investment_transaction_id = fields.Str()
    iso_currency_code = fields.Str()
    type = fields.Str()
    subtype = fields.Str()
    timestamp = fields.DateTime()