from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from marshmallow import Schema, fields

from core.models.base import Base


class Security(Base):
    __tablename__ = 'securities'

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    name = Column(String(512))
    ticker_symbol = Column(String(64))
    iso_currency_code = Column(String(8))
    institution_id = Column(String(128))
    institution_security_id = Column(String(128))
    security_id = Column(String(128))
    proxy_security_id = Column(String(128))
    cusip = Column(String(16))
    isin = Column(String(16))
    sedol = Column(String(16))
    timestamp = Column(DateTime)


class SecuritySchema(Schema):
    id = fields.Int()
    profile_id = fields.Int()
    account_id = fields.Int()
    name = fields.Str()
    ticker_symbol = fields.Str()
    iso_currency_code = fields.Str()
    institution_id = fields.Str()
    institution_security_id = fields.Str()
    security_id = fields.Str()
    proxy_security_id = fields.Str()
    cuisp = fields.Str()
    isin = fields.Str()
    sedol = fields.Str()
    timestamp = fields.DateTime()
