from sqlalchemy import Column, Integer, String, DateTime, Boolean
from core.models.base import Base


class ScheduledJob(Base):
    __tablename__ = 'scheduled_jobs'

    id = Column(Integer, primary_key=True)
    frequency_type = Column(String(64), nullable=False)
    frequency_value = Column(String(32), nullable=False)
    job_name = Column(String(128), nullable=False)
    json_args = Column(String(2048))
    last_run = Column(DateTime)
    timestamp = Column(DateTime)
