import pytest
from datetime import datetime, timezone, timedelta

from core.repositories.repository_response import RepositoryResponse
import core.actions.profile.crud as profile_crud
import core.actions.profile.auth as profile_auth
from core.actions.profile.crud import get_profile_by_email
from core.lib.jwt import check_password, decode_jwt

from api.lib.constants import API_PREFIX

from tests.factories import create_user_profile, create_reset_token
from tests.fixtures.core import db, client
from tests.fixtures.auth_fixtures import valid_register_api_request, invalid_register_api_request,\
    valid_reset_api_token, invalid_reset_api_token, valid_auth_api_request, bad_email_api_request,\
    bad_password_api_request, expired_reset_api_token


class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code


def mock_notify_profile_created(mgcfg, request):
    # thunk this so that it doesnt try to send emails
    return MockResponse(status_code=200)


@pytest.fixture(autouse=True)
def stub_emails(mocker):
    mocker.patch.object(
        profile_crud,
        'notify_profile_created',
        new=mock_notify_profile_created
    )


def test_register_accepts_valid_input(client, valid_register_api_request):
    result = client.post(f"/{API_PREFIX}/auth/register",
                         json=valid_register_api_request)
    assert result.status_code == 200
    json = result.get_json()
    assert json is not None
    assert json['id'] is not None
    assert json['email'] == valid_register_api_request['email']


def test_register_rejects_invalid_input(client, invalid_register_api_request):
    result = client.post(f"/{API_PREFIX}/auth/register",
                         json=invalid_register_api_request)
    assert result.status_code == 400
    json = result.get_json()
    assert json is not None


def test_register_rejects_duplicate_email(client, db, valid_register_api_request):
    with db.get_session() as session:
        profile = create_user_profile(
            session, email=valid_register_api_request['email'])
    result = client.post(f"/{API_PREFIX}/auth/register",
                         json=valid_register_api_request)
    assert result.status_code == 400
    json = result.get_json()


def test_login_accepts_valid_credentials(client, valid_auth_api_request):
    result = client.post(f"/{API_PREFIX}/auth/login",
                         json=valid_auth_api_request)
    assert result.status_code == 200
    json = result.get_json()
    assert json is not None
    assert json['profile'] is not None
    assert json['token'] is not None
    assert json['profile']['email'] == valid_auth_api_request['email']


def test_login_rejects_bad_username(client, bad_email_api_request):
    result = client.post(f"/{API_PREFIX}/auth/login",
                         json=bad_email_api_request)
    assert result.status_code == 404


def test_login_rejects_bad_password(client, bad_password_api_request):
    result = client.post(f"/{API_PREFIX}/auth/login",
                         json=bad_password_api_request)
    assert result.status_code == 404


def test_auth_tokens_are_valid_for_30_days(client, valid_auth_api_request):
    result = client.post(f"/{API_PREFIX}/auth/login",
                         json=valid_auth_api_request)
    assert result.status_code == 200
    json = result.get_json()
    assert json is not None
    assert json['token'] is not None
    token = decode_jwt(json['token'])
    assert datetime.fromtimestamp(token['exp'], tz=timezone.utc) > datetime.now(
        tz=timezone.utc) + timedelta(days=27)


def test_reset_password_sends_token_email(client, db, mocker):
    with db.get_session() as session:
        profile = create_user_profile(session)

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


def test_continue_reset_accepts_valid_token(client, db, valid_reset_api_token):
    p = get_profile_by_email(db, valid_reset_api_token['email'])
    assert not check_password(
        p.data.password, valid_reset_api_token['password'])
    response = client.post(f"/{API_PREFIX}/auth/reset/continue",
                           json=valid_reset_api_token)
    assert response.status_code == 204
    p = get_profile_by_email(db, valid_reset_api_token['email'])
    assert check_password(p.data.password, valid_reset_api_token['password'])


def test_continue_reset_rejects_invalid_token(client, db, invalid_reset_api_token):
    with db.get_session() as session:
        p = create_user_profile(
            session, email=invalid_reset_api_token['email'])
    with pytest.raises(Exception):
        check_password(str(p.password), invalid_reset_api_token['password'])
    response = client.post(f"/{API_PREFIX}/auth/reset/continue",
                           json=invalid_reset_api_token)
    assert response.status_code == 400
    p = get_profile_by_email(db, invalid_reset_api_token['email'])
    assert not check_password(
        p.data.password, invalid_reset_api_token['password'])


def test_continue_reset_rejects_expired_token(client, db, expired_reset_api_token):
    p = get_profile_by_email(db, expired_reset_api_token['email'])
    assert not check_password(
        p.data.password, expired_reset_api_token['password'])
    response = client.post(f"/{API_PREFIX}/auth/reset/continue",
                           json=expired_reset_api_token)
    assert response.status_code == 400
    p = get_profile_by_email(db, expired_reset_api_token['email'])
    assert not check_password(
        p.data.password, expired_reset_api_token['password'])
