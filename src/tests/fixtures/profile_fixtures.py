import pytest
from datetime import datetime, timedelta, timezone
import random

from core.models import Profile, PlaidItem
from core.schemas.profile_schemas import UpdateProfileSchema
from auth.jwt import hash_password

from tests.fixtures import *


@pytest.fixture
def profile_factory(db, faker):
    def __profile_factory(first_name=faker.first_name(),
                          last_name=faker.last_name(),
                          email=None,
                          is_admin=False,
                          password=faker.password(),
                          timestamp=datetime.now(tz=timezone.utc)):
        with db.get_session() as session:
            profile = Profile()

            profile.id = random.randint(1, 99999999)
            profile.first_name = first_name
            profile.last_name = last_name
            profile.email = email or f"{first_name}.{last_name}@{faker.unique.domain_name()}"
            profile.is_admin = is_admin
            profile.password = hash_password(password)
            profile.timestamp = timestamp

            session.add(profile)
            session.commit()
            return profile
    return __profile_factory


@pytest.fixture()
def valid_profile_update_request_factory(faker, profile_factory):
    def __request_factory(profile_id=None,
                          first_name=faker.first_name(),
                          last_name=faker.last_name()):
        if profile_id is None:
            profile_id = profile_factory().id

        return UpdateProfileSchema().load({
            'id': profile_id,
            'first_name': first_name,
            'last_name': last_name
        })
    return __request_factory


@pytest.fixture
def valid_profile_update_api_request_factory(valid_profile_update_request_factory):
    def __valid_profile_update_api_request_factory():
        request = valid_profile_update_request_factory()
        return UpdateProfileSchema().dump(request)
    return __valid_profile_update_api_request_factory


@pytest.fixture
def invalid_profile_update_api_request_factory(faker):
    def __invalid_profile_update_api_request_factory(
        email=faker.email()
    ):
        return {
            'email': email
        }
    return __invalid_profile_update_api_request_factory
