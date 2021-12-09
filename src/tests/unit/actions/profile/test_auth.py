from tests.helpers import db

from core.lib.actions.profile.auth import login, get_unauthenticated_user
from core.lib.actions.profile.requests import LoginRequest


def test_get_unauthenticated_user_returns_user(db):
    result = get_unauthenticated_user(db)

    assert result is not None
    assert result.profile is not None
    assert result.token is not None


def test_login_accepts_valid_login_request(db):
    result = login(db, LoginRequest(
        email="admin@example.org",
        password="Password1!"
    ))

    assert result is not None
    assert result.profile is not None
    assert result.token is not None


def test_login_rejects_missing_username(db):
    result = login(db, LoginRequest(
        email="",
        password="Password1!"
    ))

    assert result is None


def test_login_rejects_wrong_password(db):
    result = login(db, LoginRequest(
        email="admin@example.org",
        password="WrongPassword"
    ))

    assert result is None
