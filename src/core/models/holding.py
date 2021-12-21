from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Float
from sqlalchemy.orm import relationship

from core.models.base import Base


class Holding(Base):
    __tablename__ = 'holdings'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    security_id = Column(Integer, ForeignKey("securities.id"), nullable=False)
    cost_basis = Column(Float)
    quantity = Column(Float)
    iso_currency_code = Column(String(8))
    timestamp = Column(DateTime)

    account = relationship("Account", back_populates="holdings")
    security = relationship("Security")
    balances = relationship("HoldingBalance", back_populates="holding")
