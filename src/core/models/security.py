from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from core.models.base import Base


class Security(Base):
    __tablename__ = 'securities'

    id = Column(Integer, primary_key=True)
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
