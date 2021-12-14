from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey

from core.models.base import Base


class SecurityPrice(Base):
    __tablename__ = 'security_prices'

    id = Column(Integer, primary_key=True)
    symbol = Column(String(8), nullable=False)
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

    def to_dict(self):
        return {
            'id': self.id,
            'symbol': self.symbol,
            'high': self.high,
            'low': self.low,
            'open': self.open,
            'close': self.close,
            'volume': self.volume,
            'u_high': self.u_high,
            'u_low': self.u_low,
            'u_close': self.u_close,
            'u_volume': self.u_volume,
            'date': self.date,
            'change': self.change,
            'change_percent': self.change_percent,
            'change_over_time': self.change_over_time,
            'market_change_over_time': self.market_change_over_time,
            'resolution': self.resolution,
            'timestamp': self.timestamp
        }
