
class CreateInstantJobRequest:
    def __init__(self, job_name: str, args: dict):
        self.job_name = job_name
        self.json_args = args

