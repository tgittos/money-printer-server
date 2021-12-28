
from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.sqltypes import LargeBinary

from core.models import Base

class ApiTokenPolicy(Base):
    __tablename__ = "api_token_policies"

    id = Column(Integer, primary_key=True)
    doc = Column(String(10240), nullable=False)
    hosts = Column(String(1024), nullable=True)