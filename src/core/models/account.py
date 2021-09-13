from sqlalchemy import Column, Integer, String, DateTime, Float, ForeignKey
from core.models.base import Base


class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True)
    plaid_item_id = Column(Integer, ForeignKey("plaid_items.id"), nullable=False)
    profile_id = Column(Integer, ForeignKey("profiles.id"), nullable=False)
    account_id = Column(String(128))
    name = Column(String(64))
    official_name = Column(String(128))
    subtype = Column(String(32))
    timestamp = Column(DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'profile_id': self.profile_id,
            'name': self.name,
            'official_name': self.official_name,
            'subtype': self.subtype,
            'timestamp': self.timestamp.isoformat(),
        }
