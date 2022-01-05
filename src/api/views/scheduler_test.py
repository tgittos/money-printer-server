from rq import job
from werkzeug.datastructures import Authorization
import pytest
import json

from core.models import ScheduledJob
from core.repositories import ScheduledJobRepository
from core.lib.jwt import encode_jwt

from api.lib.constants import API_PREFIX

from tests.fixtures import *


@pytest.fixture(autouse=True)
def mock_scheduler_methods(mocker):
    mocker.patch.object(ScheduledJobRepository, 'ensure_scheduled')
    mocker.patch.object(ScheduledJobRepository, 'unschedule_job')


# /v1/api/admin/schedules
def test_create_schedule_accepts_valid_input_for_admin_token(client, admin_token_factory, valid_create_scheduled_job_api_request_factory):
    request = valid_create_scheduled_job_api_request_factory()
    token = admin_token_factory()
    response = client.post(f"/{API_PREFIX}/admin/schedules/",
                           headers={'Authorization': f"Bearer {token}"},
                           json=request)
    assert response.status_code == 201
    response_json = response.get_json()
    assert response_json['success']
    assert response_json['data']['id'] is not None
    assert response_json['data']['job_name'] == request['job_name']


# /v1/api/admin/schedules
def test_create_schedule_rejects_invalid_input_for_admin_token(client, admin_token_factory, invalid_scheduled_job_api_request):
    token = admin_token_factory()
    response = client.post(f"/{API_PREFIX}/admin/schedules/",
                           headers={'Authorization': f"Bearer {token}"},
                           json=invalid_scheduled_job_api_request)
    assert response.status_code == 400


def test_create_schedule_rejects_valid_input_for_non_admin_token(client, user_token_factory, valid_create_scheduled_job_api_request_factory):
    request = valid_create_scheduled_job_api_request_factory()
    token = user_token_factory()
    response = client.post(f"/{API_PREFIX}/admin/schedules/",
                           headers={'Authorization': f"Bearer {token}"},
                           json=request)
    assert response.status_code == 401

# /v1/api/admin/schedules/1


def test_list_schedules_returns_all_schedules_for_admin_token(db, client, admin_token_factory, scheduled_job_factory):
    token = admin_token_factory()
    job_1 = scheduled_job_factory()
    job_2 = scheduled_job_factory()
    with db.get_session() as session:
        count = session.query(ScheduledJob).count()
    response = client.get(f"/{API_PREFIX}/admin/schedules/",
                          headers={'Authorization': f"Bearer {token}"},
                          follow_redirects=True)
    assert response.status_code == 200
    response_json = response.get_json()
    assert len(response_json['data']) == count
    returned_ids = [j['id'] for j in response_json['data']]
    assert job_1.id in returned_ids
    assert job_2.id in returned_ids


# /v1/api/admin/schedules/1
def test_list_schedules_returns_401_for_non_admin(db, client, user_token_factory, scheduled_job_factory):
    token = user_token_factory()
    job_1 = scheduled_job_factory()
    job_2 = scheduled_job_factory()
    response = client.get(f"/{API_PREFIX}/admin/schedules/",
                          headers={'Authorization': f"Bearer {token}"},
                          follow_redirects=True)
    assert response.status_code == 401


# /v1/api/admin/schedules/1
def test_update_schedule_accepts_valid_input_for_admin_token(db, client, admin_token_factory, scheduled_job_factory):
    token = admin_token_factory()
    job = scheduled_job_factory()
    assert job.job_name != 'Updated Job Name'
    response = client.put(f"/{API_PREFIX}/admin/schedules/" + str(job.id),
                          headers={'Authorization': f"Bearer {token}"},
                          json={
                              'job_name': 'Updated Job Name'
    }, follow_redirects=True)
    assert response.status_code == 200
    with db.get_session() as session:
        updated_job = session.query(ScheduledJob).where(
            ScheduledJob.id == job.id).first()
        assert updated_job.job_name == 'Updated Job Name'


def updating_a_schedule_reschedules_job():
    assert False


# /v1/api/admin/schedules/1
def test_update_schedule_returns_401_for_user_token(db, client, user_token_factory, scheduled_job_factory):
    token = user_token_factory()
    job = scheduled_job_factory()
    assert job.job_name != 'Updated Job Name'
    response = client.put(f"/{API_PREFIX}/admin/schedules/" + str(job.id),
                          headers={'Authorization': f"Bearer {token}"},
                          data=json.dumps({
                              'job_name': 'Updated Job Name'
                          }),
                          content_type='application/json',
                          follow_redirects=True)
    assert response.status_code == 401
    with db.get_session() as session:
        updated_job = session.query(ScheduledJob).where(
            ScheduledJob.id == job.id).first()
    assert updated_job.job_name == job.job_name


def test_update_schedule_rejects_invalid_input(client, admin_token_factory, scheduled_job_factory, invalid_update_scheduled_job_api_request):
    token = admin_token_factory()
    job = scheduled_job_factory()
    invalid_update_scheduled_job_api_request['id'] = job.id
    result = client.put(f"/{API_PREFIX}/admin/schedules/{job.id}",
        headers={
            'Authorization': f"Bearer {token}"
        }, json = invalid_update_scheduled_job_api_request)
    assert result.status_code == 400


# /v1/api/admin/schedules/1
def test_delete_schedule_accepts_valid_input(client, admin_token_factory, scheduled_job_factory):
    token = admin_token_factory()
    job = scheduled_job_factory()
    result = client.delete(f"/{API_PREFIX}/admin/schedules/{job.id}",
        headers={
            'Authorization': f"Bearer {token}"
        })
    assert result.status_code == 200


# /v1/api/admin/schedules/1
def test_delete_schedule_rejects_invalid_input(client, admin_token_factory):
    token = admin_token_factory()
    result = client.delete(f"/{API_PREFIX}/admin/schedules/234542",
        headers={
            'Authorization': f"Bearer {token}"
        })
    assert result.status_code == 400
