from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from core.models.base import Base


class ResetToken(Base):
    __tablename__ = 'reset_tokens'

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    token = Column(String(32))
    timestamp = Column(DateTime)
    expiry = Column(DateTime)
