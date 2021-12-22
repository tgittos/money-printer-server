from sqlalchemy.sql.type_api import Emulated
import pytest

import core.lib.actions.profile.auth as auth
from core.lib.actions.profile.auth import login, get_unauthenticated_user, reset_password, continue_reset_password, get_reset_token
from core.schemas.request_schemas import RequestAuthSchema
from core.models.reset_token import ResetToken
from core.lib.actions.action_response import ActionResponse

from tests.helpers import db
from tests.factories import create_user_profile


class MockResponse(object):
    status_code = None

    def __init__(self, status_code) -> None:
        self.status_code = status_code


@pytest.fixture(autouse=True)
def mock_notifier(mocker):
    mocker.patch('core.lib.actions.profile.auth.notify_password_reset', return_value=MockResponse(
        status_code=200
    ))


@pytest.fixture()
def valid_auth_request():
    return RequestAuthSchema().load({
        'email': "user@example.org",
        'password': "Password1!"
    })


@pytest.fixture()
def invalid_auth_request():
    return RequestAuthSchema().load({
        'email': "fooo.com",
        'password': ""
    })


def test_get_unauthenticated_user_returns_user(db):
    result = get_unauthenticated_user(db)

    assert result.success
    profile, token = result.data
    assert profile is not None
    assert token is not None


def test_login_accepts_valid_login_request(db, valid_auth_request):
    s = db.get_session()
    user = create_user_profile(
        s, email="user@example.org", password="Password1!")

    result = login(db, valid_auth_request)

    assert result.success
    profile, token = result.data
    assert profile.id == user.id
    assert profile.email == user.email
    assert token is not None
    s.close()


def test_login_rejects_missing_username(db, invalid_auth_request):
    s = db.get_session()
    create_user_profile(s, email="user@example.org", password="Password1!")

    result = login(db, invalid_auth_request)

    assert not result.success
    s.close()


def test_login_rejects_wrong_password(db):
    s = db.get_session()
    create_user_profile(s, email="user@example.org", password="Password1!")

    result = login(db, RequestAuthSchema().load({
        'email': "user@example.org",
        'password': "WrongPassword"
    }))

    assert not result.success
    s.close()


def test_reset_password_creates_reset_token_with_valid_email(db):
    with db.get_session() as session:
        profile = create_user_profile(session, password="old Password 1!")
        old_count = session.query(ResetToken).count()

    result = reset_password(db, profile.email)
    assert result.success

    with db.get_session() as session:
        new_count = session.query(ResetToken).count()
        assert new_count == old_count + 1


def test_reset_password_sends_reset_token(db, mocker):
    with db.get_session() as session:
        profile = create_user_profile(session, password="old Password 1!")

    spy = mocker.spy(auth, 'notify_password_reset')

    result = reset_password(db, profile.email)
    assert result.success
    assert spy.assert_called_once()


@pytest.mark.skip(reason="need to go back and implement this")
def test_reset_password_fails_with_missing_profile(db):
    result = reset_password(db, "foo@bar.com")
    assert not result.success
    assert result.data is None


@pytest.mark.skip(reason="need to go back and implement this")
def test_continue_reset_token_accepts_valid_request(db):
    assert False


@pytest.mark.skip(reason="need to go back and implement this")
def test_continue_reset_token_rejects_expired_token(db):
    assert False


@pytest.mark.skip(reason="need to go back and implement this")
def test_continue_reset_token_rejects_missing_token(db):
    assert False
