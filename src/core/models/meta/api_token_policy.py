
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from core.models.base import Base

class ApiTokenPolicy(Base):
    __tablename__ = "api_token_policies"

    id = Column(Integer, primary_key=True)
    doc = Column(String(10240))
    hosts = Column(String(256))