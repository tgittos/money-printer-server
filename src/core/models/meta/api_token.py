from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, LargeBinary
from sqlalchemy.orm import relationship

from core.models.base import Base


class ApiToken(Base):
    __tablename__ = 'api_tokens'

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    api_token_policy_id = Column(Integer, ForeignKey("api_token_policies.id"), nullable=False)
    token = Column(LargeBinary, nullable=False)
    status = Column(String(32))
    timestamp = Column(DateTime)

    profile = relationship("Profile", back_populates="api_tokens")
    policy = relationship("ApiTokenPolicy")