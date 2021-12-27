import pytest

from core.models import ScheduledJob
from core.repositories.scheduled_job_repository import ScheduledJobRepository

from tests.fixtures import *


def get_scheduled_jobs_returns_list_of_jobs(db, scheduled_job_factory):
    with db.get_session() as session:
        scheduled_job_factory()
        scheduled_job_factory()
        count = session.query(ScheduledJob).count()
    repo = ScheduledJobRepository()
    result = repo.get_scheduled_jobs()
    assert result.success
    assert result.data is not None
    assert len(result.data) == count
    session.close()
