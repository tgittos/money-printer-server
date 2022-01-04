from marshmallow import Schema, fields

from core.models import ScheduledJob, JobResult


class CreateInstantJobSchema(Schema):
    class Meta:
        fields = ("job_name", "json_args")


class CreateScheduledJobSchema(Schema):
    class Meta:
        fields = ("cron", "job_name", "json_args", "queue", "active")


class UpdateScheduledJobSchema(Schema):
    class Meta:
        fields = ("id", "cron", "job_name", "json_args", "queue", "active")


class CreateJobResultSchema(Schema):
    class Meta:
        fields = ("job_id", "success", "log", "queue")
