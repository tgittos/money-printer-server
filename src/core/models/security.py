from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey

from core.models.base import Base


class Security(Base):
    __tablename__ = 'securities'

    id = Column(Integer, primary_key=True)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    account_id = Column(Integer, ForeignKey("accounts.id"), nullable=False)
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

    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'name': self.name,
            'ticker_symbol': self.ticker_symbol,
            'iso_currency_code': self.iso_currency_code,
            'timestamp': self.timestamp.isoformat()
        }

