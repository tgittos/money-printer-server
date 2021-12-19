from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship
from marshmallow import Schema, fields

from core.models.base import Base


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=False)
    password = Column(String(512), nullable=False)
    first_name = Column(String(32))
    last_name = Column(String(32))
    force_password_reset = Column(Boolean, nullable=False, default=True)
    is_demo_profile = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    timestamp = Column(DateTime)


class ProfileSchema(Schema):
    id = fields.Int()
    email = fields.Email()
    password = fields.Str()
    first_name = fields.Str()
    last_name = fields.Str()
    force_password_reset = fields.Bool()
    is_demo_profile = fields.Bool()
    is_admin = fields.Bool()
    timestamp = fields.DateTime()