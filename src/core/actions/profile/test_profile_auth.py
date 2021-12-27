from datetime import datetime, timedelta, timezone
from sqlalchemy.sql.type_api import Emulated
import pytest

from core.models.profile import Profile
from core.models.reset_token import ResetToken
from core.repositories import RepositoryResponse
from core.schemas.auth_schemas import LoginSchema, ResetPasswordSchema
import core.actions.profile.auth as auth
from core.actions.action_response import ActionResponse
from core.actions.profile.auth import login, get_unauthenticated_user, reset_password,\
    continue_reset_password, get_reset_token
from core.lib.jwt import check_password
from core.lib.utilities import id_generator

from tests.fixtures import *


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


@pytest.mark.focus
def test_login_accepts_valid_login_request(db, valid_auth_request_factory):
    request = valid_auth_request_factory()
    result = login(db, request)
    assert result.success
    result = result.data
    profile = result['profile']
    token = result['token']
    assert profile.email == request['email']
    assert token is not None


def test_login_rejects_missing_username(db, invalid_auth_request_factory):
    request = invalid_auth_request_factory()
    result = login(db, request)
    assert not result.success


def test_login_rejects_wrong_password(db, valid_auth_request_factory):
    request = valid_auth_request_factory()
    request['password'] = id_generator()
    result = login(db, request)
    assert not result.success


def test_reset_password_creates_reset_token_with_valid_email(db, mocker, profile_factory):
    profile = profile_factory()
    with db.get_session() as session:
        old_count = session.query(ResetToken).where(ResetToken.profile_id == profile.id).count()
    mocker.patch.object(auth, 'email_reset_token', return_value=RepositoryResponse(success=True))
    result = reset_password(db, profile.email)
    assert result.success
    with db.get_session() as session:
        new_count = session.query(ResetToken).where(ResetToken.profile_id == profile.id).count()
    assert new_count == old_count + 1


def test_reset_password_sends_reset_token(db, mocker, profile_factory):
    profile = profile_factory()
    spy = mocker.patch.object(auth, 'notify_password_reset', return_value=MockResponse(status_code=200))
    result = reset_password(db, profile.email)
    assert result.success
    spy.assert_called_once()


def test_reset_password_fails_with_missing_profile(db):
    result = reset_password(db, "foo@bar.com")
    assert not result.success
    assert result.data is None


def test_continue_reset_token_accepts_valid_request(db, valid_reset_password_request_factory):
    request = valid_reset_password_request_factory()
    result = continue_reset_password(db, request)
    assert result.success
    with db.get_session() as session:
        profile = session.query(Profile).where(
            Profile.email == request['email']).first()
    assert check_password(
        profile.password, request['password'])


def test_continue_reset_token_rejects_expired_token(db, expired_reset_password_request_factory):
    request = expired_reset_password_request_factory()
    result = continue_reset_password(db, request)
    assert not result.success


def test_continue_reset_token_rejects_missing_token(db, valid_reset_password_request_factory):
    request = valid_reset_password_request_factory()
    request['token'] = id_generator
    result = continue_reset_password(db, request)
    assert not result.success
    assert result.data is None
