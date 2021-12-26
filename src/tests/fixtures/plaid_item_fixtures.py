import pytest

from core.schemas.plaid_item_schemas import CreatePlaidItemSchema, UpdatePlaidItemSchema

from tests.factories import create_plaid_item
from tests.fixtures.core import db
from tests.fixtures.profile_fixtures import existing_profile


@pytest.fixture
def existing_plaid_item(db, existing_profile):
    with db.get_session() as session:
        return create_plaid_item(
            session,
            profile_id=existing_profile.id
        )


@pytest.fixture
def valid_create_request(existing_profile):
    return CreatePlaidItemSchema().load({
        'profile_id': existing_profile.id,
        'item_id': 'thisisanitemid',
        'access_token': 'thisistheaccesstoken',
        'request_id': 'therequestid',
        'status': ''
    })


@pytest.fixture
def valid_update_request(existing_plaid_item):
    return UpdatePlaidItemSchema().load({
        'id': existing_plaid_item.id,
        'status': 'updated'
    })
