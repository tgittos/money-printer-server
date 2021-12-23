from datetime import datetime, timedelta, timezone
from sqlalchemy.sql.type_api import Emulated
import pytest

import core.lib.actions.profile.auth as auth
from core.lib.actions.profile.auth import login, get_unauthenticated_user, reset_password, continue_reset_password, get_reset_token
from core.schemas.read_schemas import ReadProfileSchema
from core.schemas.request_schemas import RequestAuthSchema, RequestPasswordResetSchema
from core.models.profile import Profile
from core.models.reset_token import ResetToken
from core.lib.jwt import check_password
from core.lib.actions.action_response import ActionResponse

from tests.helpers import db
from tests.factories import create_user_profile, create_reset_token


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


@pytest.fixture()
def valid_reset_password_request(db):
    with db.get_session() as session:
        profile = create_user_profile(session)
        token = create_reset_token(session, profile_id=profile.id)
    return RequestPasswordResetSchema().load({
        'profile': ReadProfileSchema().dump(profile),
        'token': token.token,
        'password': 'my new password1!'
    })


@pytest.fixture()
def expired_reset_password_request(db):
    with db.get_session() as session:
        profile = create_user_profile(session)
        token = create_reset_token(session,
                                   profile_id=profile.id,
                                   expiry=datetime.now(
                                       tz=timezone.utc) - timedelta(days=45))
    return RequestPasswordResetSchema().load({
        'profile': ReadProfileSchema().dump(profile),
        'token': token.token,
        'password': 'my new password1!'
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
            Profile.id == valid_reset_password_request['profile']['id']).first()

    assert check_password(
        profile.password, valid_reset_password_request['password'])


def test_continue_reset_token_rejects_expired_token(db, expired_reset_password_request):
    result = continue_reset_password(db, expired_reset_password_request)
    assert not result.success


def test_continue_reset_token_rejects_missing_token(db):
    with db.get_session() as session:
        profile = create_user_profile(session)

    result = continue_reset_password(db, RequestPasswordResetSchema().load({
        'profile': ReadProfileSchema().dump(profile),
        'token': 'foobarfaketoken',
        'password': 'my new password1!'
    }))

    assert not result.success
    assert result.data is None
