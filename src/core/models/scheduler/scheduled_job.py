from sqlalchemy import Column, Integer, String, DateTime, Boolean
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

    def to_dict(self):
        return {
            'id': self.id,
            'cron': self.cron,
            'job_name': self.job_name,
            'json_args': self.json_args,
            'last_run': self.last_run,
            'queue': self.queue,
            'active': self.active,
            'timestamp': self.timestamp
        }
