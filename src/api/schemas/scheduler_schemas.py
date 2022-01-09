from marshmallow import Schema, fields

from core.models import ScheduledJob, JobResult
from api.flask_app import ma


class ReadScheduledJobApiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = ScheduledJob
        include_fk = True


class ReadJobResultApiSchema(ma.SQLAlchemyAutoSchema):
    class Meta:
        model = JobResult
        include_fk = True


read_scheduled_job_schema = ReadScheduledJobApiSchema()
read_scheduled_jobs_schema = ReadScheduledJobApiSchema(many=True)

read_job_result_schema = ReadJobResultApiSchema()
read_job_results_schema = ReadJobResultApiSchema(many=True)