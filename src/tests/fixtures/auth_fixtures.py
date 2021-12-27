import pytest
from datetime import datetime, timezone, timedelta

from core.models import ResetToken
from core.schemas.auth_schemas import RegisterProfileSchema, LoginSchema, ResetPasswordSchema
from core.lib.jwt import encode_jwt
from core.lib.utilities import id_generator

from tests.fixtures.core import db, factory
from tests.fixtures.profile_fixtures import profile_factory


@pytest.fixture
def reset_token_factory(db, factory, faker):
    def __reset_token_factory(profile_id=None,
                              token=faker.md5(),
                              expiry=datetime.now(
                                  tz=timezone.utc) + timedelta(days=30),
                              timestamp=datetime.now(tz=timezone.utc)):
        with db.get_session() as session:
            t = ResetToken()
            t.token = token
            t.profile_id = profile_id
            t.expiry = expiry
            t.timestamp = timestamp

            session.add(t)
            session.commit()
            factory.append(t)

            return t
    return __reset_token_factory


@pytest.fixture
def user_token_factory(db, profile_factory):
    def __user_token_factory(profile_id=None):
        if profile_id is None:
            profile_id = profile_factory(is_admin=False).id
        token = encode_jwt(profile=profile_id)
        return token
    return __user_token_factory


@pytest.fixture
def admin_token_factory(db, profile_factory):
    def __admin_token_factory(profile_id=None):
        if profile_id is None:
            profile_id = profile_factory(is_admin=True).id
        token = encode_jwt(profile=profile_id)
        return token
    return __admin_token_factory


@pytest.fixture()
def valid_register_request(faker):
    return RegisterProfileSchema().load({
        'email': faker.email(),
        'first_name': faker.first_name(),
        'last_name': faker.last_name()
    })


@pytest.fixture()
def valid_auth_request_factory(profile_factory):
    def __valid_auth_request_factory(profile=None, password=None):
        if profile is None:
            password = id_generator(size=8)
            profile = profile_factory(password=password)
        return LoginSchema().load({
            'email': profile.email,
            'password': password
        })
    return __valid_auth_request_factory


@pytest.fixture()
def invalid_auth_request(faker):
    return LoginSchema().load({
        'email': faker.email(),
        'password': ""
    })


@pytest.fixture()
def valid_reset_password_request_factory(db, profile_factory, reset_token_factory):
    def __valid_reset_password_request(profile=None,
                                       password=None):
        if password is None:
            password = id_generator(size=8)
        if profile is None:
            with db.get_session() as session:
                profile = profile_factory(password=password)
        token = reset_token_factory(profile_id=profile.id)
        return ResetPasswordSchema().load({
            'email': profile.email,
            'token': token.token,
            'password': password
        })
    return __valid_reset_password_request


@pytest.fixture()
def expired_reset_password_request_factory(db, profile_factory, reset_token_factory):
    def __expired_reset_password_request(profile=None,
                                         password=None,
                                         expiry=datetime.now(tz=timezone.utc) - timedelta(days=45)):
        if password is None:
            password = id_generator(size=8)
        if profile is None:
            with db.get_session() as session:
                profile = profile_factory(password=password)
        token = reset_token_factory(profile_id=profile.id, expiry=expiry)
        return ResetPasswordSchema().load({
            'email': profile.email,
            'token': token.token,
            'password': password
        })
    return __expired_reset_password_request


@ pytest.fixture
def valid_register_api_request(faker):
    return {
        'email': faker.email(),
        'first_name': faker.first_name(),
        'last_name': faker.last_name()
    }


@pytest.fixture
def invalid_register_api_request(faker):
    return {
        'email': faker.email(),
        'first_name': faker.name()
    }


@pytest.fixture
def valid_auth_api_request(valid_auth_request_factory):
    request = valid_auth_request_factory()
    return LoginSchema().dump(request)


@pytest.fixture
def bad_password_api_request(valid_auth_request_factory):
    request = valid_auth_request_factory()
    request['password'] = id_generator(size=8)
    return LoginSchema().dump(request)


@pytest.fixture
def bad_email_api_request(faker):
    return {
        'email': faker.email(),
        'password': id_generator(size=8)
    }


@pytest.fixture
def valid_reset_api_token(valid_reset_password_request_factory):
    request = valid_reset_password_request_factory()
    return ResetPasswordSchema().dump(request)


@pytest.fixture
def expired_reset_api_token(expired_reset_password_request_factory):
    request = expired_reset_password_request_factory()
    return ResetPasswordSchema().dump(request)


@pytest.fixture
def invalid_reset_api_token(faker):
    return {
        'email': faker.email(),
        'token': id_generator(size=8),
        'password': id_generator(size=8)
    }
