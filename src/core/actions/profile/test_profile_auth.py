from datetime import datetime, timedelta, timezone
from sqlalchemy.sql.type_api import Emulated
import pytest

from core.models.profile import Profile
from core.models.reset_token import ResetToken
from core.schemas.auth_schemas import LoginSchema, ResetPasswordSchema
import core.actions.profile.auth as auth
from core.actions.profile.auth import login, get_unauthenticated_user, reset_password,\
    continue_reset_password, get_reset_token
from core.lib.jwt import check_password

from tests.factories import create_user_profile, create_reset_token
from tests.fixtures.core import db
from tests.fixtures.auth_fixtures import invalid_auth_request, valid_auth_request, valid_reset_password_request,\
    expired_reset_password_request


class MockResponse(object):
    status_code = None

    def __init__(self, status_code) -> None:
        self.status_code = status_code


@pytest.fixture(autouse=True)
def mock_notifier(mocker):
    mocker.patch('core.actions.profile.auth.notify_password_reset', return_value=MockResponse(
        status_code=200
    ))


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
    result = result.data
    profile = result['profile']
    token = result['token']
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

    result = login(db, LoginSchema().load({
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
    spy.assert_called_once()


def test_reset_password_fails_with_missing_profile(db):
    result = reset_password(db, "foo@bar.com")
    assert not result.success
    assert result.data is None


def test_continue_reset_token_accepts_valid_request(db, valid_reset_password_request):
    result = continue_reset_password(db, valid_reset_password_request)
    assert result.success

    with db.get_session() as session:
        profile = session.query(Profile).where(
            Profile.email == valid_reset_password_request['email']).first()

    assert check_password(
        profile.password, valid_reset_password_request['password'])


def test_continue_reset_token_rejects_expired_token(db, expired_reset_password_request):
    result = continue_reset_password(db, expired_reset_password_request)
    assert not result.success


def test_continue_reset_token_rejects_missing_token(db):
    with db.get_session() as session:
        profile = create_user_profile(session)

    result = continue_reset_password(db, ResetPasswordSchema().load({
        'email': profile.email,
        'token': 'foobarfaketoken',
        'password': 'my new password1!'
    }))

    assert not result.success
    assert result.data is None
