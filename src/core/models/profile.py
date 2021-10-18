from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from core.models.base import Base


class Profile(Base):
    __tablename__ = 'profiles'

    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=False)
    password = Column(String(512), nullable=False)
    first_name = Column(String(32))
    last_name = Column(String(32))
    force_password_reset = Column(Boolean, nullable=False, default=True)
    is_demo_profile = Column(Boolean, nullable=False, default=False)
    is_admin = Column(Boolean, nullable=False, default=False)
    timestamp = Column(DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'timestamp': self.timestamp.isoformat(),
            'is_demo': self.is_demo_profile,
            'is_admin': self.is_admin
        }

