
class CreateScheduledJobRequest:
    def __init__(self, job_name: str, frequency_type: str, frequency_value: str, json_args: dict):
        self.job_name = job_name
        self.frequency_type = frequency_type
        self.frequency_value = frequency_value
        self.json_args = json_args


class CreateInstantJobRequest:
    def __init__(self, job_name: str, args: dict):
        self.job_name = job_name
        self.args = args

