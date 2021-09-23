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

    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'available': self.available,
            'current': self.current,
            'iso_currency_code': self.iso_currency_code,
            'timestamp': self.timestamp.isoformat(),
        }
