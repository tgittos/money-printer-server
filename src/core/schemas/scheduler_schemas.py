from marshmallow import Schema, fields


class CreateInstantJobSchema(Schema):
    class Meta:
        fields = ("job_name", "json_args")


class CreateScheduledJobSchema(Schema):
    class Meta:
        fields = ("cron", "job_name", "json_args", "queue", "active")


class ReadScheduledJobSchema(Schema):
    result = fields.Nested('ReadJobResultSchema')

    class Meta:
        additional = ("id", "cron", "job_name", "json_args",
                      "last_run", "queue", "active", "timestamp")


class UpdateScheduledJobSchema(Schema):
    class Meta:
        fields = ("id", "cron", "job_name", "json_args", "queue", "active")


class CreateJobResultSchema(Schema):
    class Meta:
        fields = ("job_id", "success", "log", "queue")


class ReadJobResultSchema(Schema):
    class Meta:
        fields = ("id", "job_id", "success", "log", "queue", "timestamp")
