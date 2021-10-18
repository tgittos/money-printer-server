from sqlalchemy import Column, Integer, String, DateTime, Boolean
from core.models.base import Base


class JobResult(Base):
    __tablename__ = 'job_results'

    id = Column(Integer, primary_key=True)
    job_id = Column(String(128), nullable=False)
    success = Column(Boolean, nullable=False)
    log = Column(String(5120))
    queue = Column(String(128), nullable=False)
    timestamp = Column(DateTime)

    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'success': self.success,
            'log': self.log,
            'queue': self.queue,
            'timestamp': self.timestamp
        }
