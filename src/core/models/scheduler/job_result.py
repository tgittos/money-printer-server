from sqlalchemy import Column, Integer, String, DateTime, Boolean
from marshmallow import Schema, fields

from core.models.base import Base


class JobResult(Base):
    __tablename__ = 'job_results'

    id = Column(Integer, primary_key=True)
    job_id = Column(String(128), nullable=False)
    success = Column(Boolean, nullable=False)
    log = Column(String(5120))
    queue = Column(String(128), nullable=False)
    timestamp = Column(DateTime)


class JobResultSchema(Schema):
    id = fields.Int()
    job_id = fields.Str()
    success = fields.Bool()
    log = fields.Str()
    queue = fields.Str()
    timestamp = fields.DateTime()