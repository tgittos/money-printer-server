from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from core.models.base import Base


class InvestmentTransaction(Base):
    __tablename__ = 'investment_transactions'

    id = Column(Integer, primary_key=True)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    name = Column(String(512))
    amount = Column(Float)
    fees = Column(Float)
    price = Column(Float)
    quantity = Column(Float)
    date = Column(DateTime)
    investment_transaction_id = Column(String(256))
    iso_currency_code = Column(String(8))
    type = Column(String(32))
    subtype = Column(String(32))
    timestamp = Column(DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'name': self.name,
            'amount': self.amount,
            'fees': self.fees,
            'price': self.price,
            'quantity': self.quantity,
            'date': self.date.isoformat(),
            'iso_currency_code': self.iso_currency_code,
            'type': self.type,
            'subtype': self.subtype,
            'timestamp': self.timestamp.isoformat(),
        }
