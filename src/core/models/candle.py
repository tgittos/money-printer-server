from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, DateTime, Float

Base = declarative_base()

# class Candle(Base):
#     __tablename__ = 'candles'
#
#     id = Column(Integer, primary_key=True)
#     symbol = Column(String(10))
#     resolution = Column(String(3))
#     timestamp = Column(DateTime)
#     open = Column(Float)
#     close = Column(Float)
#     high = Column(Float)
#     low = Column(Float)
#     volume = Column(Integer)

#     def as_dict(self):
#         return {
#             't': self.timestamp,
#             'o': self.open,
#             'c': self.close,
#             'h': self.high,
#             'l': self.low,
#             'v': self.volume
#         }