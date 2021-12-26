import pytest
from datetime import datetime, timezone, timedelta

from core.schemas.auth_schemas import RegisterProfileSchema, LoginSchema, ResetPasswordSchema
from core.lib.jwt import encode_jwt

from tests.fixtures.core import db
from tests.factories import create_user_profile, create_reset_token


@pytest.fixture()
def valid_register_request():
    return RegisterProfileSchema().load({
        'email': "tgittos@moneyprintergoesbrr.io",
        'first_name': "Tim",
        'last_name': "Gittos"
    })


@pytest.fixture()
def valid_auth_request():
    return LoginSchema().load({
        'email': "user@example.org",
        'password': "Password1!"
    })


@pytest.fixture()
def invalid_auth_request():
    return LoginSchema().load({
        'email': "fooo.com",
        'password': ""
    })


@pytest.fixture()
def valid_reset_password_request(db):
    with db.get_session() as session:
        profile = create_user_profile(session)
        token = create_reset_token(session, profile_id=profile.id)
    return ResetPasswordSchema().load({
        'email': profile.email,
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
    return ResetPasswordSchema().load({
        'email': profile.email,
        'token': token.token,
        'password': 'my new password1!'
    })


@pytest.fixture
def valid_register_api_request():
    return {
        'email': 'hello@example.com',
        'first_name': 'Hello',
        'last_name': 'World'
    }


@pytest.fixture
def invalid_register_api_request():
    return {
        'email': 'foo.com',
        'first_name': 'Fake'
    }


@pytest.fixture
def valid_auth_api_request(db):
    with db.get_session() as session:
        profile = create_user_profile(session, password="this is my password")
    return {
        'email': profile.email,
        'password': 'this is my password'
    }


@pytest.fixture
def bad_password_api_request(db):
    with db.get_session() as session:
        profile = create_user_profile(session, password="this is my password")
    return {
        'email': profile.email,
        'password': 'this is not my password'
    }


@pytest.fixture
def bad_email_api_request(db):
    return {
        'email': 'doesnt@exist.com',
        'password': 'doesnt matter'
    }


@pytest.fixture
def valid_reset_api_token(db):
    with db.get_session() as session:
        profile = create_user_profile(session)
        token = create_reset_token(session, profile_id=profile.id)
    return {
        'email': profile.email,
        'token': token.token,
        'password': 'my new password'
    }


@pytest.fixture
def expired_reset_api_token(db):
    with db.get_session() as session:
        profile = create_user_profile(session)
        token = create_reset_token(
            session,
            profile_id=profile.id,
            expiry=datetime.now(tz=timezone.utc) - timedelta(days=1))
    return {
        'email': profile.email,
        'token': token.token,
        'password': 'my new password'
    }


@pytest.fixture
def invalid_reset_api_token(db):
    return {
        'email': 'user@example.org',
        'token': 'this token doesnt exist',
        'password': 'my new password'
    }


@pytest.fixture()
def user_token(db):
    # seed a profile and gen up a token for that profile
    session = db.get_session()
    profile = create_user_profile(
        session, email="user@example.org", is_admin=False)
    token = encode_jwt(profile=profile)
    session.close()
    return token


@pytest.fixture()
def admin_token(db):
    # seed a profile and gen up a token for that profile
    session = db.get_session()
    profile = create_user_profile(
        session, email="admin@example.org", is_admin=True)
    token = encode_jwt(profile=profile)
    session.close()
    return token
