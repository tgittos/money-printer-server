from sqlalchemy import Column, Integer, String, DateTime, Boolean
from sqlalchemy.orm import relationship

from core.models.base import Base


class ScheduledJob(Base):
    __tablename__ = 'scheduled_jobs'

    id = Column(Integer, primary_key=True)
    cron = Column(String(32), nullable=False)
    job_name = Column(String(128), nullable=False)
    json_args = Column(String(2048))
    last_run = Column(DateTime)
    queue = Column(String(128), nullable=False)
    active = Column(Boolean, nullable=False, default=True)
    timestamp = Column(DateTime)

    results = relationship("JobResult", back_populates="scheduled_job")