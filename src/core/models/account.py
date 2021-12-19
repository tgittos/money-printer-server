from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields

from core.models.base import Base


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    plaid_item_id = Column(Integer, ForeignKey("plaid_items.id"), nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    account_id = Column(String(128))
    name = Column(String(256))
    official_name = Column(String(256))
    type = Column(String(32))
    subtype = Column(String(32))
    timestamp = Column(DateTime)


class AccountSchema(Schema):
    id = fields.Int()
    plaid_item_id = fields.Int()
    profile_id = fields.Int()
    account_id = fields.Int()
    name = fields.Str()
    official_name = fields.Str()
    type = fields.Str()
    subtype = fields.Str()
    timestamp = fields.DateTime()

