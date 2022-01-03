import pytest
from datetime import datetime, timezone

from core.models import ApiToken, ApiTokenPolicy
from core.schemas.api_schemas import *
from core.lib.jwt import generate_temp_password, hash_password

from tests.fixtures import *


@pytest.fixture()
def api_token_policy_factory(db):
    def __api_token_policy_factory(
        doc="",  # TODO - replace this with a static default generator or something
        hosts=None
    ):
        with db.get_session() as session:
            policy = ApiTokenPolicy()
            policy.id = random.randint(1, 50000)
            policy.doc = doc
            policy.hosts = hosts
            policy.timestamp = datetime.now(tz=timezone.utc)

            session.add(policy)
            session.commit()
            return policy
    return __api_token_policy_factory


@pytest.fixture()
def api_token_factory(db, faker, profile_factory, api_token_policy_factory):
    def __api_token_factory(
        profile_id=None,
        token=generate_temp_password(),
        api_token_policy_id=None,
        status="good_standing",
    ):
        if profile_id is None:
            profile_id = profile_factory().id
        if api_token_policy_id is None:
            api_token_policy_id = api_token_policy_factory().id
        with db.get_session() as session:
            token_obj = ApiToken()
            token.id = random.randint(1, 50000)
            token_obj.profile_id = profile_id
            token_obj.api_token_policy_id = api_token_policy_id
            token_obj.token = hash_password(token)
            token_obj.status = status
            token_obj.timestamp = datetime.now(tz=timezone.utc)

            session.add(token_obj)
            session.commit()
            return token_obj
    return __api_token_factory


@pytest.fixture()
def valid_api_token_create_request_factory(profile_factory, api_token_policy_factory):
    def __request_factory(
        profile_id=None,
        token=generate_temp_password(),
        api_token_policy_id=None,
        status="good_standing"
    ):
        if profile_id is None:
            profile_id = profile_factory().id
        if api_token_policy_id is None:
            api_token_policy_id = api_token_policy_factory().id
        return CreateApiKeySchema().load({
            'profile_id': profile_id,
            'token': token,
            'api_token_policy_id': api_token_policy_id,
            'status': status
        })
    return __request_factory


@pytest.fixture()
def valid_api_token_update_request_factory(api_token_factory):
    def __request_factory(
        id=None,
        api_token_policy_id=None,
        status="rate_limited"
    ):
        if id is None:
            id = api_token_factory().id
        return UpdateApiKeySchema().load({
            'id': id,
            'api_token_policy_id': api_token_policy_id,
            'status': status
        })
    return __request_factory


@pytest.fixture()
def valid_api_token_policy_create_request_factory(faker):
    def __request_factory(
        doc="",  # TODO
        hosts=[faker.unique.host_name()]
    ):
        return CreateApiKeyPolicySchema().load({
            'doc': doc,
            'hosts': hosts
        })
    return __request_factory


@pytest.fixture()
def valid_api_token_policy_update_request_factory(faker):
    def __request_factory(
        doc="",  # TODO
        hosts=[faker.unique.host_name()]
    ):
        return UpdateApiKeyPolicySchema().load({
            'doc': doc,
            'hosts': hosts
        })
    return __request_factory


@pytest.fixture()
def valid_api_token_create_api_request_factory(valid_api_token_create_request_factory):
    def __request_factory():
        request = valid_api_token_create_request_factory()
        return CreateApiKeySchema().dump(request)
    return __request_factory


@pytest.fixture()
def valid_api_token_update_api_request_factory(valid_api_token_update_request_factory):
    def __request_factory():
        request = valid_api_token_update_request_factory()
        return UpdateApiKeySchema().dump(request)
    return __request_factory


@pytest.fixture()
def valid_api_token_policy_create_api_request_factory(valid_api_token_policy_create_request_factory):
    def __request_factory():
        request = valid_api_token_policy_create_request_factory()
        return CreateApiKeyPolicySchema().dump(request)
    return __request_factory


@pytest.fixture()
def valid_api_token_policy_update_api_request_factory(valid_api_token_policy_update_request_factory):
    def __request_factory():
        request = valid_api_token_policy_update_request_factory()
        return UpdateApiKeyPolicySchema().dump(request)
    return __request_factory
