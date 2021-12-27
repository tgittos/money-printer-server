import pytest
from datetime import datetime, timezone, timedelta

from core.repositories.repository_response import RepositoryResponse
import core.actions.profile.crud as profile_crud
import core.actions.profile.auth as profile_auth
from core.actions.profile.crud import get_profile_by_email
from core.lib.jwt import check_password, decode_jwt

from api.lib.constants import API_PREFIX

from tests.fixtures import *


@pytest.fixture(autouse=True)
def stub_emails(mocker):
    mocker.patch.object(
        profile_crud,
        'notify_profile_created',
        new=mock_notify_profile_created
    )


def test_register_accepts_valid_input(client, valid_register_api_request_factory):
    request = valid_register_api_request_factory()
    result = client.post(f"/{API_PREFIX}/auth/register",
                         json=request)
    assert result.status_code == 200
    json = result.get_json()
    assert json is not None
    assert json['id'] is not None
    assert json['email'] == request['email']


def test_register_rejects_invalid_input(client, invalid_register_api_request_factory):
    request = invalid_register_api_request_factory()
    result = client.post(f"/{API_PREFIX}/auth/register",
                         json=request)
    assert result.status_code == 400
    json = result.get_json()
    assert json is not None


def test_register_rejects_duplicate_email(client, db, profile_factory, valid_register_api_request_factory):
    request = valid_register_api_request_factory()
    profile = profile_factory()
    request['email'] = profile.email
    result = client.post(f"/{API_PREFIX}/auth/register",
                         json=request)
    assert result.status_code == 400
    json = result.get_json()


def test_login_accepts_valid_credentials(client, valid_auth_api_request_factory):
    request = valid_auth_api_request_factory()
    result = client.post(f"/{API_PREFIX}/auth/login",
                         json=request)
    assert result.status_code == 200
    json = result.get_json()
    assert json is not None
    assert json['profile'] is not None
    assert json['token'] is not None
    assert json['profile']['email'] == request['email']


def test_login_rejects_bad_username(client, bad_email_api_request_factory):
    request = bad_email_api_request_factory()
    result = client.post(f"/{API_PREFIX}/auth/login",
                         json=request)
    assert result.status_code == 404


def test_login_rejects_bad_password(client, bad_password_api_request_factory):
    request = bad_password_api_request_factory()
    result = client.post(f"/{API_PREFIX}/auth/login",
                         json=request)
    assert result.status_code == 404


def test_auth_tokens_are_valid_for_30_days(client, valid_auth_api_request_factory):
    request = valid_auth_api_request_factory()
    result = client.post(f"/{API_PREFIX}/auth/login",
                         json=request)
    assert result.status_code == 200
    json = result.get_json()
    assert json is not None
    assert json['token'] is not None
    token = decode_jwt(json['token'])
    assert datetime.fromtimestamp(token['exp'], tz=timezone.utc) > datetime.now(
        tz=timezone.utc) + timedelta(days=27)


def test_reset_password_sends_token_email(client, db, mocker, profile_factory):
    profile = profile_factory()
    spy = mocker.patch.object(profile_auth, 'email_reset_token')
    response = client.post(f"/{API_PREFIX}/auth/reset", json={
        'email': profile.email
    })
    assert response.status_code == 204
    spy.assert_called_once()


def test_reset_password_accepts_bad_email_but_doesnt_send_token(client, db, mocker):
    spy = mocker.patch.object(profile_auth, 'email_reset_token')

    response = client.post(f"/{API_PREFIX}/auth/reset", json={
        'email': 'bad@email.com'
    })

    assert response.status_code == 204
    spy.assert_not_called()


def test_continue_reset_accepts_valid_token(client, db, valid_reset_api_token_factory):
    request = valid_reset_api_token_factory()
    p = get_profile_by_email(db, request['email'])
    assert not check_password(
        p.data.password, request['password'])
    response = client.post(f"/{API_PREFIX}/auth/reset/continue",
                           json=request)
    assert response.status_code == 204
    p = get_profile_by_email(db, request['email'])
    assert check_password(p.data.password, request['password'])


def test_continue_reset_rejects_invalid_token(client, db, profile_factory, invalid_reset_api_token_factory):
    request = invalid_reset_api_token_factory()
    profile = profile_factory()
    request['email'] = profile.email
    with pytest.raises(Exception):
        check_password(str(profile.password),
                       request['password'])
    response = client.post(f"/{API_PREFIX}/auth/reset/continue",
                           json=request)
    assert response.status_code == 400
    p = get_profile_by_email(db, request['email'])
    assert not check_password(
        p.data.password, request['password'])


def test_continue_reset_rejects_expired_token(client, db, expired_reset_api_token_factory):
    request = expired_reset_api_token_factory()
    p = get_profile_by_email(db, request['email'])
    assert not check_password(
        p.data.password, request['password'])
    response = client.post(f"/{API_PREFIX}/auth/reset/continue",
                           json=request)
    assert response.status_code == 400
    p = get_profile_by_email(db, request['email'])
    assert not check_password(
        p.data.password, request['password'])
