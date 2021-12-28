import pytest
from datetime import datetime, timedelta, timezone

from core.models import PlaidItem
from core.schemas.plaid_item_schemas import CreatePlaidItemSchema, UpdatePlaidItemSchema

from tests.fixtures.core import db
from tests.fixtures.profile_fixtures import profile_factory


@pytest.fixture
def plaid_item_factory(db, faker, profile_factory):
    def __plaid_item_factory(profile_id=None,
                             item_id=faker.md5(),
                             access_token=faker.md5(),
                             request_id=faker.md5(),
                             status='',
                             timestamp=datetime.now(tz=timezone.utc)):
        with db.get_session() as session:
            if profile_id is None:
                profile = profile_factory()
                profile_id = profile.id

            plaid_item = PlaidItem()
            plaid_item.item_id = item_id
            plaid_item.profile_id = profile_id
            plaid_item.access_token = access_token
            plaid_item.item_id = item_id
            plaid_item.status = status
            plaid_item.request_id = request_id
            plaid_item.timestamp = timestamp

            session.add(plaid_item)
            session.commit()
            return plaid_item
    return __plaid_item_factory


@pytest.fixture
def valid_plaid_item_create_request_factory(faker, profile_factory):
    def __request_factory(profile_id=None,
                          item_id=faker.md5(),
                          access_token=faker.md5(),
                          request_id=faker.md5(),
                          status=''):
        if profile_id is None:
            profile_id = profile_factory().id
        return CreatePlaidItemSchema().load({
            'profile_id': profile_id,
            'item_id': item_id,
            'access_token': access_token,
            'request_id': request_id,
            'status': status
        })
    return __request_factory


@pytest.fixture
def valid_plaid_item_update_request_factory(faker, plaid_item_factory):
    def __request_factory(plaid_item_id=None, status='updated'):
        if plaid_item_id is None:
            plaid_item_id = plaid_item_factory().id
        return UpdatePlaidItemSchema().load({
            'id': plaid_item_id,
            'status': status
        })
    return __request_factory
