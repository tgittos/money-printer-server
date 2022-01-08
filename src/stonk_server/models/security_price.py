from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from .base import Base


class SecurityPrice(Base):
    __tablename__ = 'security_prices'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(64), ForeignKey("securities.symbol"))
    high = Column(Float)
    low = Column(Float)
    open = Column(Float)
    close = Column(Float)
    volume = Column(Integer)
    u_high = Column(Float)
    u_low = Column(Float)
    u_open = Column(Float)
    u_close = Column(Float)
    u_volume = Column(Integer)
    date = Column(DateTime)
    change = Column(Float)
    change_percent = Column(Float)
    change_over_time = Column(Float)
    market_change_over_time = Column(Float)
    resolution = Column(String(32), nullable=False)
    timestamp = Column(DateTime)

    security = relationship("Security", back_populates="prices")
