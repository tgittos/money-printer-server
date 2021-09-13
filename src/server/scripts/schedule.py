import json


if __name__ == '__main__':
    from script_base import *
    from server.config import config as server_config
    from core.apis.mailgun import MailGunConfig
    from core.repositories.scheduled_job_repository import ScheduledJobRepository, ScheduledJobRepositoryConfig, CreateScheduledJobRequest

    repo = ScheduledJobRepository(ScheduledJobRepositoryConfig(
        mailgun_config=MailGunConfig(api_key=server_config['mailgun']['api_key'],
                                     domain=server_config['mailgun']['domain']),
        mysql_config=app_config['db']
    ))

    job_name = input("Name of job to schedule: ")
    frequency_type = input("Desired frequency [hourly|daily|weekly]: ")
    frequency_value = input("How frequent [every n/frequency periods]: ")

    result = repo.create_scheduled_job(CreateScheduledJobRequest(
        job_name=job_name,
        frequency_type=frequency_type,
        frequency_value=frequency_value
    ))

    if result is not None:
        print("Successfully scheduled job: {0}".format(json.dumps(result)))
    else:
        print("Something went wrong!")


