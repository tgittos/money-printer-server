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

    def to_dict(self):
        return {
            'id': self.id,
            'account_id': self.account_id,
            'security_id': self.security_id,
            'cost_basis': self.cost_basis,
            'quantity': self.quantity,
            'iso_currency_code': self.iso_currency_code,
            'timestamp': self.timestamp.isoformat()
        }

