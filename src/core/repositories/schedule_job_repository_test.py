import pytest

from tests.fixtures.core import db
from tests.factories import create_scheduled_job

from core.repositories.scheduled_job_repository import ScheduledJobRepository


def get_scheduled_jobs_returns_list_of_jobs(db):
    session = db.get_session()
    job_1 = create_scheduled_job(session, job_name='Job 1')
    job_2 = create_scheduled_job(session, job_name='Job 2')
    repo = ScheduledJobRepository()
    result = repo.get_scheduled_jobs()
    assert result.success
    assert result.data is not None
    assert len(result.data) == 2
    session.close()
