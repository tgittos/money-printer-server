from tests.helpers import client, db
from tests.factories import create_user_profile


def test_get_profile_returns_authed_profile():
    assert False


def test_update_profile_accepts_valid_input():
    assert False


def test_update_rejects_invalid_input():
    assert False


def test_sync_profile(db, client):
    session = db.get_session()
    profile = create_user_profile(session)
