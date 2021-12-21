from sqlalchemy.sql.type_api import Emulated
import pytest

from core.lib.actions.profile.auth import login, get_unauthenticated_user
from core.schemas.request_schemas import RequestAuthSchema
from tests.helpers import db
from tests.factories import create_user_profile


@pytest.fixture()
def valid_auth_request():
    return RequestAuthSchema().load({
        'email':"user@example.org",
        'password':"Password1!"
    })

@pytest.fixture()
def invalid_auth_request():
    return RequestAuthSchema().load({
        'email':"fooo.com",
        'password':""
    })


def test_get_unauthenticated_user_returns_user(db):
    result = get_unauthenticated_user(db)

    assert result.success
    profile, token = result.data
    assert profile is not None
    assert token is not None


def test_login_accepts_valid_login_request(db, valid_auth_request):
    s = db.get_session()
    user = create_user_profile(s, email="user@example.org", password="Password1!")

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
        'email':"user@example.org",
        'password':"WrongPassword"
    }))

    assert not result.success
    s.close()
