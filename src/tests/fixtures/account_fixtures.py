import pytest
from datetime import datetime, timezone

from core.models import Account
from core.schemas.account_schemas import *
from core.lib.utilities import id_generator

from tests.fixtures import *


@pytest.fixture
def account_factory(db, faker, profile_factory, plaid_item_factory):
    def __factory(
        profile_id=None,
        plaid_item_id=None,
        account_id=id_generator(size=8),
        name=f"{faker.name()} Account",
        official_name=id_generator(),
        type='savings',
        subtype=''
    ):
        if profile_id is None:
            profile_id = profile_factory().id
        if plaid_item_id is None:
            plaid_item_id = plaid_item_factory(profile_id=profile_id).id
        with db.get_session() as session:
            account = Account()

            account.profile_id = profile_id
            account.plaid_item_id = plaid_item_id
            account.account_id = account_id
            account.name = name
            account.official_name = official_name
            account.type = type
            account.subtype = subtype
            account.timestamp = datetime.now(tz=timezone.utc)

            session.add(account)
            session.commit()

            return account
    return __factory


@pytest.fixture
def valid_create_account_request_factory(db, faker, profile_factory, plaid_item_factory):
    def __factory(
        profile_id=None,
        plaid_item_id=None,
        account_id=id_generator(size=8),
        name=f"{faker.name()} Account",
        official_name=id_generator(),
        type='savings',
        subtype=''
    ):
        if profile_id is None:
            profile_id = profile_factory().id
        if plaid_item_id is None:
            plaid_item_id = plaid_item_factory().id
        return CreateAccountSchema().load({
            'profile_id': profile_id,
            'plaid_item_id': plaid_item_id,
            'account_id': account_id,
            'name': name,
            'official_name': official_name,
            'type': type,
            'subtype': subtype
        })

    return __factory


@pytest.fixture
def valid_update_account_request_factory(db, faker, profile_factory, account_factory):
    def __factory(
        profile_id=None,
        account_id=None,
        name=f"{faker.name()} Account",
        account_account_id=id_generator(size=8),
        official_name=id_generator(),
        type='checking',
        subtype=''
    ):
        if profile_id is None:
            profile_id = profile_factory().id
        if account_id is None:
            account_id = account_factory(profile_id=profile_id).id
        return UpdateAccountSchema().load({
            'id': account_id,
            'profile_id': profile_id,
            'account_id': account_account_id,
            'name': name,
            'official_name': official_name,
            'type': type,
            'subtype': subtype
        })

    return __factory
