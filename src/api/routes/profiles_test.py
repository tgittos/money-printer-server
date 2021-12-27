import pytest

from core.lib.jwt import encode_jwt
from core.repositories.scheduled_job_repository import ScheduledJobRepository

from api.lib.constants import API_PREFIX

from tests.fixtures.core import client, db, factory
from tests.fixtures.profile_fixtures import profile_factory, valid_profile_update_api_request,\
    invalid_profile_update_api_request
from tests.fixtures.auth_fixtures import user_token_factory, admin_token_factory
from tests.fixtures.plaid_item_fixtures import plaid_item_factory


@pytest.fixture()
def instant_job_spy(mocker):
    return mocker.patch.object(
        ScheduledJobRepository,
        'create_instant_job'
    )


def test_get_profile_returns_authed_profile(client, profile_factory, user_token_factory):
    profile = profile_factory()
    token = user_token_factory(profile_id=profile.id)
    response = client.get(f"/{API_PREFIX}/profile",
                          headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 200
    json = response.get_json()
    assert json is not None
    assert json['email'] == profile.email


def test_get_profile_fails_with_no_token(client):
    response = client.get(f"/{API_PREFIX}/profile")
    assert response.status_code == 401


def test_update_profile_accepts_valid_input(client, profile_factory, user_token_factory, valid_profile_update_api_request):
    profile = profile_factory()
    token = user_token_factory(profile_id=profile.id)
    response = client.put(f"/{API_PREFIX}/profile",
                          headers={'Authorization': f"Bearer {token}"},
                          json=valid_profile_update_api_request)
    assert response.status_code == 200
    json = response.get_json()
    assert json is not None
    assert json['first_name'] == valid_profile_update_api_request['first_name']
    assert json['last_name'] == valid_profile_update_api_request['last_name']


def test_update_rejects_invalid_input(client, profile_factory, user_token_factory, invalid_profile_update_api_request):
    profile = profile_factory()
    token = user_token_factory(profile_id=profile.id)
    invalid_profile_update_api_request['email'] = profile.email
    response = client.put(f"/{API_PREFIX}/profile",
                          headers={'Authorization': f"Bearer {token}"},
                          json=invalid_profile_update_api_request)
    assert response.status_code == 400


def test_sync_profile_schedules_instant_job(db, client, profile_factory, plaid_item_factory, user_token_factory, instant_job_spy):
    profile = profile_factory()
    token = user_token_factory(profile_id=profile.id)
    item = plaid_item_factory(profile_id=profile.id)
    response = client.post(f"/{API_PREFIX}/profile/sync",
                           headers={'Authorization': f"Bearer {token}"})
    assert response.status_code == 204
    instant_job_spy.assert_called_once()
