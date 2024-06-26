import pytest
from datetime import datetime, timezone, timedelta
import random

from core.models import ResetToken
from core.schemas.auth_schemas import RegisterProfileSchema, LoginSchema, ResetPasswordSchema
from core.lib.utilities import id_generator
from auth.jwt import encode_jwt

from tests.fixtures.core import db
from tests.fixtures.profile_fixtures import profile_factory


@pytest.fixture
def reset_token_factory(db, faker):
    def __reset_token_factory(profile_id=None,
                              token=faker.md5(),
                              expiry=datetime.now(
                                  tz=timezone.utc) + timedelta(days=30),
                              timestamp=datetime.now(tz=timezone.utc)):
        with db.get_session() as session:
            t = ResetToken()

            t.id = random.randint(1, 99999999)
            t.token = token
            t.profile_id = profile_id
            t.expiry = expiry
            t.timestamp = timestamp

            session.add(t)
            session.commit()

            return t
    return __reset_token_factory


@pytest.fixture
def user_token_factory(db, profile_factory):
    def __user_token_factory(profile=None):
        if profile is None:
            profile = profile_factory(is_admin=False)
        token = encode_jwt(profile=profile)
        return token
    return __user_token_factory


@pytest.fixture
def admin_token_factory(db, profile_factory):
    def __admin_token_factory(profile=None):
        if profile is None:
            profile = profile_factory(is_admin=True)
        token = encode_jwt(profile=profile)
        return token
    return __admin_token_factory


@pytest.fixture()
def valid_register_request_factory(faker):
    def __valid_register_request_factory(
        email=None,
        first_name=faker.first_name(),
        last_name=faker.last_name()
    ):
        args = {
            'email': email or f"{first_name}.{last_name}@{faker.unique.domain_name()}",
            'first_name': first_name,
            'last_name': last_name
        }
        return RegisterProfileSchema().load(args)
    return __valid_register_request_factory


@pytest.fixture()
def valid_auth_request_factory(profile_factory):
    def __valid_auth_request_factory(profile=None, password=None):
        if profile is None:
            password = id_generator(size=8)
            profile = profile_factory(password=password)
        args = {
            'email': profile.email,
            'password': password
        }
        return LoginSchema().load(args)
    return __valid_auth_request_factory


@pytest.fixture()
def invalid_auth_request_factory(faker):
    def __invalid_auth_request_factory(
        email=faker.email(),
        password=""
    ):
        return LoginSchema().load({
            'email': email,
            'password': password
        })
    return __invalid_auth_request_factory


@pytest.fixture()
def valid_reset_password_request_factory(db, profile_factory, reset_token_factory):
    def __valid_reset_password_request(profile=None,
                                       password=None):
        old_password = id_generator(size=8)
        if profile is None:
            profile = profile_factory(password=old_password)
        if password is None:
            password = id_generator(size=8)
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
        old_password = id_generator(size=8)
        if password is None:
            password = id_generator(size=8)
        if profile is None:
            profile = profile_factory(password=old_password)
        token = reset_token_factory(profile_id=profile.id, expiry=expiry)
        return ResetPasswordSchema().load({
            'email': profile.email,
            'token': token.token,
            'password': password
        })
    return __expired_reset_password_request


@ pytest.fixture
def valid_register_api_request_factory(faker):
    def __valid_register_api_request_factory(
        email=None,
        first_name=faker.first_name(),
        last_name=faker.last_name()
    ):
        return {
            'email': email or f"{first_name}.{last_name}@{faker.unique.domain_name()}",
            'first_name': first_name,
            'last_name': last_name
        }
    return __valid_register_api_request_factory


@pytest.fixture
def invalid_register_api_request_factory(faker):
    def __invalid_register_api_request_factory(
        email=faker.email(),
        first_name=faker.name()
    ):
        return {
            'email': email,
            'first_name': first_name
        }
    return __invalid_register_api_request_factory


@pytest.fixture
def valid_auth_api_request_factory(valid_auth_request_factory):
    def __valid_auth_api_request_factory():
        request = valid_auth_request_factory()
        return LoginSchema().dump(request)
    return __valid_auth_api_request_factory


@pytest.fixture
def bad_password_api_request_factory(valid_auth_request_factory):
    def __bad_password_api_request_factory():
        request = valid_auth_request_factory()
        request['password'] = id_generator(size=8)
        return LoginSchema().dump(request)
    return __bad_password_api_request_factory


@pytest.fixture
def bad_email_api_request_factory(faker):
    def __bad_email_api_request_factory(
        email=faker.email(),
        password=id_generator(size=8)
    ):
        return {
            'email': email,
            'password': password
        }
    return __bad_email_api_request_factory


@pytest.fixture
def valid_reset_api_token_factory(valid_reset_password_request_factory):
    def __valid_reset_api_token_factory():
        request = valid_reset_password_request_factory()
        return ResetPasswordSchema().dump(request)
    return __valid_reset_api_token_factory


@pytest.fixture
def expired_reset_api_token_factory(expired_reset_password_request_factory):
    def __expired_reset_api_token_factory():
        request = expired_reset_password_request_factory()
        return ResetPasswordSchema().dump(request)
    return __expired_reset_api_token_factory


@pytest.fixture
def invalid_reset_api_token_factory(faker):
    def __invalid_reset_api_token_factory(
        email=faker.email(),
        token=id_generator(size=8),
        password=id_generator(size=8)
    ):
        return {
            'email': email,
            'token': token,
            'password': password
        }
    return __invalid_reset_api_token_factory
