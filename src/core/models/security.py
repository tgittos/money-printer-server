from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql.expression import null

from core.models.base import Base


class Security(Base):
    __tablename__ = 'securities'

    symbol = Column(String(64), primary_key=True, nullable=False)
    name = Column(String(512))
    iso_currency_code = Column(String(8))
    institution_id = Column(String(128))
    institution_security_id = Column(String(128))
    security_id = Column(String(128))
    proxy_security_id = Column(String(128))
    cusip = Column(String(16))
    isin = Column(String(16))
    sedol = Column(String(16))
    timestamp = Column(DateTime)

    prices = relationship("SecurityPrice", back_populates="security")
