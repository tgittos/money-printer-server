from sqlalchemy import Column, Integer, String, DateTime, Boolean, LargeBinary
from sqlalchemy.orm import relationship

from core.models.base import Base


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=False)
    password = Column(LargeBinary, nullable=False)
    first_name = Column(String(32))
    last_name = Column(String(32))
    force_password_reset = Column(Boolean, nullable=False, default=True)
    is_demo_profile = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    timestamp = Column(DateTime)

    plaid_items = relationship("PlaidItem", back_populates="profile")
    accounts = relationship("Account", back_populates="profile")
    api_tokens = relationship("ApiToken", back_populates="profile")
