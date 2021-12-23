import pytest

import core.lib.actions.profile.crud as profile_crud
from core.repositories.repository_response import RepositoryResponse

from tests.factories import create_user_profile, create_reset_token
from tests.helpers import db, client


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


@pytest.fixture
def valid_register_request():
    return {
        'email': 'hello@example.com',
        'first_name': 'Hello',
        'last_name': 'World'
    }


@pytest.fixture
def invalid_register_request():
    return {
        'email': 'foo.com',
        'first_name': 'Fake'
    }


@pytest.fixture
def valid_auth_request(db):
    with db.get_session() as session:
        profile = create_user_profile(session, password="this is my password")
    return {
        'email': profile.email,
        'password': 'this is my password'
    }


@pytest.fixture
def bad_password_request(db):
    with db.get_session() as session:
        profile = create_user_profile(session, password="this is my password")
    return {
        'email': profile.email,
        'password': 'this is not my password'
    }


@pytest.fixture
def bad_email_request(db):
    return {
        'email': 'doesnt@exist.com',
        'password': 'doesnt matter'
    }


@pytest.fixture
def valid_reset_token(db):
    with db.get_session() as session:
        profile = create_user_profile(session)
        token = create_reset_token(session, profile_id=profile.id)
    return {
        'token': token.token,
        'password': 'my new password'
    }


@pytest.fixture
def invalid_reset_token(db):
    return {
        'token': 'this token doesnt exist',
        'password': 'my new password'
    }


def test_register_accepts_valid_input(client, valid_register_request):
    result = client.post('v1/api/auth/register', json=valid_register_request)
    assert result.status_code == 200
    json = result.get_json()
    assert json is not None
    assert json['id'] is not None
    assert json['email'] == valid_register_request['email']


def test_register_rejects_invalid_input(client, invalid_register_request):
    result = client.post('v1/api/auth/register', json=invalid_register_request)
    assert result.status_code == 400
    json = result.get_json()
    assert json is not None


def test_register_rejects_duplicate_email(client, db, valid_register_request):
    with db.get_session() as session:
        profile = create_user_profile(session, email=valid_register_request['email'])
    result = client.post('v1/api/auth/register', json=valid_register_request)
    assert result.status_code == 400
    json = result.get_json()


def test_login_accepts_valid_credentials(client, valid_auth_request):
    result = client.post('v1/api/auth/login', json=valid_auth_request)
    assert result.status_code == 200
    json = result.get_json()
    assert json is not None
    assert json['profile'] is not None
    assert json['token'] is not None
    assert json['profile']['email'] == valid_auth_request['email']


def test_login_rejects_bad_username(client, bad_email_request):
    result = client.post('v1/api/auth/login', json=bad_email_request)
    assert result.status_code == 404


def test_login_rejects_bad_password(client, bad_password_request):
    result = client.post('v1/api/auth/login', json=bad_password_request)
    assert result.status_code == 404


def test_auth_tokens_are_valid_for_30_days(client, valid_auth_request):
    assert False


def test_reset_password_sends_token_email(client, db):
    assert False


def test_reset_password_accepts_bad_email_but_doesnt_send_token(client, db):
    assert False


def test_continue_reset_accepts_valid_token(client, db, valid_reset_token):
    assert False


def test_continue_reset_rejects_invalid_token(client, db, invalid_reset_token):
    assert False
