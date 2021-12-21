from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from core.models.base import Base


class HoldingBalance(Base):
    __tablename__ = 'holding_balances'

    id = Column(Integer, primary_key=True)
    holding_id = Column(Integer, ForeignKey("holdings.id"), nullable=False)
    cost_basis = Column(Float)
    quantity = Column(Float)
    timestamp = Column(DateTime)

    holding = relationship("Holding", back_populates="balances")
