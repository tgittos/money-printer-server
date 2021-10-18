
class CreateScheduledJobRequest:
    def __init__(self, job_name: str, cron: str, json_args: dict):
        self.job_name = job_name
        self.cron = cron
        self.json_args = json_args


class CreateInstantJobRequest:
    def __init__(self, job_name: str, args: dict):
        self.job_name = job_name
        self.args = args

