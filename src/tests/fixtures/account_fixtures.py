import pytest
import random
from datetime import datetime, time, timezone

from core.models import Account, AccountBalance
from core.schemas.account_schemas import *
from core.schemas.account_balance_schemas import *
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

            account.id = random.randint(1, 99999999)
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
def account_balance_factory(db, faker, account_factory):
    def __account_balance_factory(
        account_id=None,
        available=random.random() * 1000,
        current=random.random() * 1000,
        iso_currency_code='usd',
        timestamp=datetime.now(tz=timezone.utc)
    ):
        if account_id is None:
            account_id = account_factory().id
        with db.get_session() as session:
            balance = AccountBalance()

            balance.id = random.randint(1, 50000)
            balance.account_id = account_id
            balance.available = available
            balance.current = current
            balance.iso_currency_code = iso_currency_code
            balance.timestamp = timestamp

            session.add(balance)
            session.commit()
            return balance
    return __account_balance_factory


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
            plaid_item_id = plaid_item_factory(profile_id=profile_id).id
        return CreateAccountSchema().load({
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
            'account_id': account_account_id,
            'name': name,
            'official_name': official_name,
            'type': type,
            'subtype': subtype
        })

    return __factory


@pytest.fixture
def valid_create_account_balance_request_factory(account_factory):
    def __valid_create_account_balance_request_factory(
        account_id=None,
        available=random.random() * 1000,
        current=random.random() * 1000,
        iso_currency_code='usd'
    ):
        if account_id is None:
            account_id = account_factory().id
        return CreateAccountBalanceSchema().load({
            'account_id': account_id,
            'available': available,
            'current': current,
            'iso_currency_code': iso_currency_code
        })
    return __valid_create_account_balance_request_factory


@pytest.fixture
def valid_create_account_api_request_factory(faker, valid_create_account_request_factory):
    def __factory(
        profile_id=None,
        plaid_item_id=None,
        account_id=id_generator(size=8),
        name=f"{faker.name()} Account",
        official_name=id_generator(),
        type='savings',
        subtype=''
    ):
        request = valid_create_account_request_factory(
            profile_id=profile_id,
            plaid_item_id=plaid_item_id,
            account_id=account_id,
            name=name,
            official_name=official_name,
            type=type,
            subtype=subtype
        )
        return CreateAccountSchema().dump(request)
    return __factory


@pytest.fixture
def valid_update_account_api_request_factory(faker, valid_update_account_request_factory):
    def __factory(
        profile_id=None,
        account_id=None,
        name=f"{faker.name()} Account",
        account_account_id=id_generator(size=8),
        official_name=id_generator(),
        type='checking',
        subtype=''
    ):
        request = valid_update_account_request_factory(
            profile_id=profile_id,
            account_id=account_id,
            account_account_id=account_account_id,
            name=name,
            official_name=official_name,
            type=type,
            subtype=subtype
        )
        return UpdateAccountSchema().dump(request)
    return __factory


@pytest.fixture
def valid_create_account_balance_api_request_factory(valid_create_account_balance_request_factory):
    def __valid_create_account_balance_api_request_factory(
        account_id=None,
        available=random.random() * 1000,
        current=random.random() * 1000,
        iso_currency_code='usd'
    ):
        request = valid_create_account_balance_request_factory(
            account_id=account_id,
            available=available,
            current=current,
            iso_currency_code=iso_currency_code
        )
        return CreateAccountBalanceSchema().load(request)
    return __valid_create_account_balance_api_request_factory
