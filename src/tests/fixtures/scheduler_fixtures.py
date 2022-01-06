import pytest
import random

from core.models import ScheduledJob
from core.schemas.scheduler_schemas import CreateScheduledJobSchema, CreateInstantJobSchema,\
    UpdateScheduledJobSchema
from core.lib.constants import WORKER_QUEUE

from tests.fixtures.core import db


@pytest.fixture
def scheduled_job_factory(db, faker):
    def __scheduled_job_factory(
            job_name=f"{' '.join(faker.words())} Job",
            json_args={},
            cron='0 0 12 1/1 * ? *',
            active=True,
            queue=WORKER_QUEUE):
        with db.get_session() as session:
            job = ScheduledJob()

            job.id = random.randint(1, 99999999)
            job.job_name = job_name
            job.cron = cron
            job.json_args = json_args
            job.active = active
            job.queue = queue

            session.add(job)
            session.commit()

            return job
    return __scheduled_job_factory


@pytest.fixture()
def valid_create_scheduled_job_request_factory(faker):
    def __valid_create_scheduled_job_request_factory(
        job_name=f"{' '.join(faker.words())} Job",
        cron="0 * * * *",
        json_args={}
    ):
        return CreateScheduledJobSchema().load({
            'job_name': job_name,
            'cron': cron,
            'json_args': json_args
        })
    return __valid_create_scheduled_job_request_factory


@pytest.fixture()
def valid_create_instant_job_request_factory(faker):
    def __valid_create_instant_job_request_factory(
        job_name=f"{' '.join(faker.words())} Job",
        json_args={}
    ):
        return CreateInstantJobSchema().load({
            'job_name': job_name,
            'json_args': json_args
        })
    return __valid_create_instant_job_request_factory


@pytest.fixture()
def valid_update_scheduled_job_request_factory(faker, scheduled_job_factory):
    def __valid_update_scheduled_job_request_factory(
        job_id=None,
        job_name=f"{' '.join(faker.words())} Job",
        cron="0 * * * *",
        json_args={}
    ):
        if job_id is None:
            job_id = scheduled_job_factory().id
        return UpdateScheduledJobSchema().load({
            'id': job_id,
            'job_name': job_name,
            'cron': cron,
            'json_args': json_args
        })
    return __valid_update_scheduled_job_request_factory


@pytest.fixture
def valid_create_scheduled_job_api_request_factory(valid_create_scheduled_job_request_factory):
    def __factory():
        request = valid_create_scheduled_job_request_factory()
        return CreateScheduledJobSchema().dump(request)
    return __factory


@pytest.fixture
def valid_create_instant_job_api_request_factory(valid_create_instant_job_request_factory):
    def __factory():
        request = valid_create_instant_job_request_factory()
        return CreateInstantJobSchema().dump(request)
    return __factory


@pytest.fixture
def valid_update_scheduled_job_api_request_factory(faker, valid_update_scheduled_job_request_factory):
    def __factory(
            job_id: None,
            job_name=f"{' '.join(faker.words())} Job",
            cron="0 * * * *",
            json_args={}):
        request = valid_update_scheduled_job_request_factory(
            job_id=job_id,
            job_name=job_name,
            cron=cron,
            json_args=json_args)
        return UpdateScheduledJobSchema().dump(request)


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


@pytest.fixture()
def invalid_update_scheduled_job_api_request():
    return {
        'job_name': "",
        'cron': None
    }
