import pytest

from core.models import ScheduledJob
from core.schemas.scheduler_schemas import CreateScheduledJobSchema, CreateInstantJobSchema
from core.lib.constants import WORKER_QUEUE

from tests.fixtures.core import db, factory


@pytest.fixture
def scheduled_job_factory(db, factory, faker):
    def __scheduled_job_factory(
            job_name=f"{faker.words().join(' ')} Job",
            json_args={},
            cron='0 0 12 1/1 * ? *',
            active=True,
            queue=WORKER_QUEUE):
        with db.get_session() as session:
            job = ScheduledJob()
            job.job_name = job_name
            job.cron = cron
            job.json_args = json_args
            job.active = active
            job.queue = queue
            session.add(job)
            session.commit()
            factory.append(job)
            return job
    return __scheduled_job_factory


@pytest.fixture()
def valid_create_scheduled_job_request(faker):
    return CreateScheduledJobSchema().load({
        'job_name': f"{faker.words().join(' ')} Job",
        'cron': "0 * * * *",
        'json_args': {}
    })


@pytest.fixture()
def valid_create_instant_job_request(faker):
    return CreateInstantJobSchema().load({
        'job_name': f"{faker.words().join(' ')} Job",
        'json_args': {}
    })


@pytest.fixture
def valid_create_scheduled_job_api_request(valid_create_scheduled_job_request):
    return CreateScheduledJobSchema().dump(valid_create_scheduled_job_request)


@pytest.fixture
def valid_create_instant_job_api_request(valid_create_instant_job_request):
    return CreateInstantJobSchema().dump(valid_create_instant_job_request)


@pytest.fixture()
def invalid_instant_job_api_request():
    return {
        'job_name': "",
        'json_args': None
    }


@pytest.fixture()
def invalid_scheduled_job_api_request():
    return {
        'job_name': "",
        'cron': None,
        'json_args': ""
    }
