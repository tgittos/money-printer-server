from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from core.models.base import Base


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    plaid_item_id = Column(Integer, ForeignKey("plaid_items.id"), nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    account_id = Column(String(128))
    name = Column(String(256))
    official_name = Column(String(256))
    type = Column(String(32))
    subtype = Column(String(32))
    timestamp = Column(DateTime)

    profile = relationship("Profile", back_populates="accounts")
    plaid_item = relationship("PlaidItem", back_populates="accounts")
    balances = relationship("AccountBalance", back_populates="account")
    holdings = relationship("Holding", back_populates="account")
    transactions = relationship("InvestmentTransaction", back_populates="account")
