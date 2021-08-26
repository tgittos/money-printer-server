from sqlalchemy import Column, Integer, String, DateTime, Boolean
from core.models.base import Base


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=False)
    password = Column(512, nullable=False)
    first_name = Column(String(32))
    last_name = Column(String(32))
    force_password_reset = Column(Boolean, nullable=False, default=True)
    timestamp = Column(DateTime)

