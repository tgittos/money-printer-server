from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from core.models.base import Base


class Balance(Base):
    __tablename__ = 'balances'

    id = Column(Integer, primary_key=True)
    accountId = Column(Integer, ForeignKey("accounts.id"), nullable=False)
    available = Column(Float)
    current = Column(Float)
    iso_currency_code = Column(String(8))
    timestamp = Column(DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.accountId,
            'available': self.available,
            'current': self.current,
            'iso_currency_code': self.iso_currency_code,
            'timestamp': self.timestamp.isoformat(),
        }
