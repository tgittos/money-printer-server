import pytest
import json

from tests.helpers import client, db
from tests.factories import create_scheduled_job, create_user_profile

from core.models.scheduler.scheduled_job import ScheduledJob
from core.lib.jwt import encode_jwt
from api.routes.scheduler import ScheduledJobRepository

# return client.post('/login', data=dict(
#        username=username,
#        password=password
#    ), follow_redirects=True)

#rv = c.post('/api/auth', json={
#        'email': 'flask@example.com', 'password': 'secret'
#    })
#    json_data = rv.get_json()

@pytest.fixture(autouse=True)
def mock_scheduler_methods(mocker):
    mocker.patch.object(ScheduledJobRepository, 'ensure_scheduled')
    mocker.patch.object(ScheduledJobRepository, 'unschedule_job')


@pytest.fixture()
def admin_token(db):
    # seed a profile and gen up a token for that profile
    session = db.get_session()
    profile = create_user_profile(session, is_admin=True)
    token = encode_jwt(profile=profile)
    session.close()
    return token


@pytest.fixture()
def user_token(db):
    # seed a profile and gen up a token for that profile
    session = db.get_session()
    profile = create_user_profile(session)
    token = encode_jwt(profile=profile)
    session.close()
    return token


# /v1/api/admin/schedules
def test_create_schedule_accepts_valid_input(client):
    assert False


# /v1/api/admin/schedules
def test_create_schedule_rejects_invalid_input(client):
    assert False


# /v1/api/admin/schedules/1
def test_list_schedules_returns_all_schedules_for_admin(db, client, admin_token):
    session = db.get_session()
    job_1 = create_scheduled_job(session)
    job_2 = create_scheduled_job(session)
    response = client.get('/v1/api/admin/schedules',
                          headers={'Authorization': f"Bearer {admin_token}"},
                          follow_redirects=True)
    assert response.status_code == 200
    response_json = response.get_json()
    assert len(response_json['data']) == 2
    for json in response_json['data']:
        assert json['id'] in [job_1.id, job_2.id]
        assert json['job_name'] in [job_1.job_name, job_2.job_name]
    session.close()


# /v1/api/admin/schedules/1
def test_list_schedules_returns_401_for_non_admin(db, client, user_token):
    session = db.get_session()
    job_1 = create_scheduled_job(session)
    job_2 = create_scheduled_job(session)
    response = client.get('/v1/api/admin/schedules',
                          headers={'Authorization': f"Bearer {user_token}"},
                          follow_redirects=True)
    assert response.status_code == 401
    session.close()


# /v1/api/admin/schedules/1
def test_update_schedule_accepts_valid_input_for_admin_token(db, client, admin_token):
    session = db.get_session()
    job = create_scheduled_job(session)
    session.close()
    assert job.job_name != 'Updated Job Name'
    response = client.put('/v1/api/admin/schedules/' + str(job.id),
                          headers={'Authorization': f"Bearer {admin_token}"},
                          data=json.dumps({
                              'job_name':'Updated Job Name'
                          }),
                          content_type='application/json',
                          follow_redirects=True)
    assert response.status_code == 200
    session = db.get_session()
    updated_job = session.query(ScheduledJob).where(ScheduledJob.id == job.id).first()
    assert updated_job.job_name == 'Updated Job Name'
    session.close()


def updating_a_schedule_reschedules_job():
    assert False


# /v1/api/admin/schedules/1
def test_update_schedule_returns_401_for_user_token(db, client, user_token):
    session = db.get_session()
    job = create_scheduled_job(session)
    assert job.job_name != 'Updated Job Name'
    response = client.put('/v1/api/admin/schedules/' + str(job.id),
                          headers={'Authorization': f"Bearer {user_token}"},
                          data=json.dumps({
                              'job_name':'Updated Job Name'
                          }),
                          content_type='application/json',
                          follow_redirects=True)
    assert response.status_code == 401
    updated_job = session.query(ScheduledJob).where(ScheduledJob.id == job.id).first()
    assert updated_job.job_name == job.job_name
    session.close()

# /v1/api/admin/schedules/1
def test_update_schedule_rejects_invalid_input(client):
    assert False


# /v1/api/admin/schedules/1
def test_delete_schedule_accepts_valid_input(client):
    assert False


# /v1/api/admin/schedules/1
def test_delete_schedule_rejects_invalid_input(client):
    assert False
