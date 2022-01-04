from marshmallow import Schema, fields

from core.models import ScheduledJob, JobResult
from api.lib.globals import marshmallow_app as ma


class ReadScheduledJobSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ScheduledJob
        include_fk = True


class ReadJobResultSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = JobResult
        include_fk = True


read_scheduled_job_schema = ReadScheduledJobSchema()
read_scheduled_jobs_schema = ReadScheduledJobSchema(many=True)

read_job_result_schema = ReadJobResultSchema()
read_job_results_schema = ReadJobResultSchema(many=True)