import pytest

from core.lib.jwt import encode_jwt
from core.repositories.scheduled_job_repository import ScheduledJobRepository

from tests.helpers import client, db
from tests.factories import create_user_profile, create_plaid_item


@pytest.fixture()
def instant_job_spy(mocker):
    return mocker.patch.object(
        ScheduledJobRepository,
        'create_instant_job'
    )


@pytest.fixture()
def user_token(db):
    # seed a profile and gen up a token for that profile
    session = db.get_session()
    profile = create_user_profile(
        session, email="user@example.org", is_admin=False)
    token = encode_jwt(profile=profile)
    session.close()
    return token


@pytest.fixture
def valid_profile_update_request():
    return {
        'first_name': 'New First',
        'last_name': 'New Last'
    }


@pytest.fixture
def invalid_profile_update_request():
    return {
        'email': 'my_new_email@example.com'
    }


def test_get_profile_returns_authed_profile(client, user_token):
    response = client.get('/v1/api/profile',
                          headers={'Authorization': f"Bearer {user_token}"})
    assert response.status_code == 200
    json = response.get_json()
    assert json is not None
    assert json['email'] == 'user@example.org'


def test_get_profile_fails_with_no_token(client):
    response = client.get('/v1/api/profile')
    assert response.status_code == 401


def test_update_profile_accepts_valid_input(client, user_token, valid_profile_update_request):
    response = client.put('/v1/api/profile',
                          headers={'Authorization': f"Bearer {user_token}"},
                          json=valid_profile_update_request)
    assert response.status_code == 200
    json = response.get_json()
    assert json is not None
    assert json['first_name'] == valid_profile_update_request['first_name']
    assert json['last_name'] == valid_profile_update_request['last_name']


def test_update_rejects_invalid_input(client, user_token, invalid_profile_update_request):
    response = client.put('/v1/api/profile',
                          headers={'Authorization': f"Bearer {user_token}"},
                          json=invalid_profile_update_request)
    assert response.status_code == 400


def test_sync_profile_schedules_instant_job(db, client, user_token, instant_job_spy):
    with db.get_session() as session:
        # this is brittle af
        create_plaid_item(session=session, profile_id=1)
    response = client.post('/v1/api/profile/sync',
                           headers={'Authorization': f"Bearer {user_token}"})
    assert response.status_code == 204
    instant_job_spy.assert_called_once()
