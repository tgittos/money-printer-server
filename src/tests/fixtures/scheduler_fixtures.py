import pytest


@pytest.fixture()
def valid_scheduled_job_request():
    return {
        'job_name': "My New Job",
        'cron': "0 * * * *",
        'json_args': "{}"
    }


@pytest.fixture()
def invalid_scheduled_job_request():
    return {
        'job_name': "",
        'cron': None,
        'json_args': ""
    }


@pytest.fixture()
def valid_instant_job_request():
    return {
        'job_name': "Once off job",
        'json_args': {}
    }


@pytest.fixture()
def invalid_instant_job_request():
    return {
        'job_name': "",
        'json_args': None
    }
