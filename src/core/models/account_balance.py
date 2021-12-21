from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from core.models.base import Base


class AccountBalance(Base):
    __tablename__ = 'account_balances'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    available = Column(Float)
    current = Column(Float)
    iso_currency_code = Column(String(8))
    timestamp = Column(DateTime)

    account = relationship("Account", back_populates="balances")
