from sqlalchemy import Column, Integer, String, DateTime, Boolean
from marshmallow import Schema, fields

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

class CreateScheduledJobSchema(Schema):
    cron = fields.Str(required=True)
    job_name = fields.Str(required=True)
    json_args = fields.Str()


class ScheduledJobSchema(Schema):
    id = fields.Int()
    cron = fields.Str()
    job_name = fields.Str()
    json_args = fields.Str()
    last_run = fields.DateTime()
    queue = fields.Str()
    active = fields.Bool()
    timestamp = fields.DateTime()
