from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship

from core.models.base import Base


class JobResult(Base):
    __tablename__ = 'job_results'

    id = Column(Integer, primary_key=True)
    scheduled_job_id = Column(Integer, ForeignKey("scheduled_jobs.id") ,nullable=False)
    job_id = Column(String(128), nullable=False)
    success = Column(Boolean, nullable=False)
    log = Column(String(5120))
    queue = Column(String(128), nullable=False)
    timestamp = Column(DateTime)

    scheduled_job = relationship("ScheduledJob", back_populates="results")
