from core.lib.actions.profile.auth import login, get_unauthenticated_user
from core.lib.actions.profile.requests import LoginRequest
from tests.helpers import db
from tests.factories import create_user_profile


def test_get_unauthenticated_user_returns_user(db):
    result = get_unauthenticated_user(db)

    assert result is not None
    assert result.profile is not None
    assert result.token is not None


def test_login_accepts_valid_login_request(db):
    s = db.get_session()
    user = create_user_profile(s, email="user@example.org", password="Password1!")

    result = login(db, LoginRequest(
        email="user@example.org",
        password="Password1!"
    ))

    assert result is not None
    assert result.profile == user.to_dict()
    assert result.token is not None
    s.close()


def test_login_rejects_missing_username(db):
    s = db.get_session()
    create_user_profile(s, email="user@example.org", password="Password1!")

    result = login(db, LoginRequest(
        email="",
        password="Password1!"
    ))

    assert result is None
    s.close()


def test_login_rejects_wrong_password(db):
    s = db.get_session()
    create_user_profile(s, email="user@example.org", password="Password1!")

    result = login(db, LoginRequest(
        email="user@example.org",
        password="WrongPassword"
    ))

    assert result is None
    s.close()
