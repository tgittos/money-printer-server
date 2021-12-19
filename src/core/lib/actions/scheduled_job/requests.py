
class CreateScheduledJobRequest:
    def __init__(self, job_name: str, cron: str, args: dict):
        self.job_name = job_name
        self.cron = cron
        self.json_args = args


class CreateInstantJobRequest:
    def __init__(self, job_name: str, args: dict):
        self.job_name = job_name
        self.json_args = args

