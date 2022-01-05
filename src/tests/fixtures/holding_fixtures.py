import pytest
import random
import string
from datetime import datetime, timezone

from core.models import Holding, HoldingBalance
from core.schemas.holding_schemas import *
from core.schemas.holding_balance_schemas import *

from tests.fixtures import *


@pytest.fixture
def holding_factory(db, faker, account_factory, security_factory):
    def __holding_factory(
        account_id=None,
        security_symbol=None,
        cost_basis=random.random() * 5,
        quantity=random.randint(1, 500),
        iso_currency_code='USD'
    ):
        if account_id is None:
            account_id = account_factory().id
        if security_symbol is None:
            security_symbol = security_factory().symbol

        with db.get_session() as session:
            holding = Holding()

            holding.id = random.randint(1, 50000)
            holding.account_id = account_id
            holding.security_symbol = security_symbol
            holding.cost_basis = cost_basis
            holding.quantity = quantity
            holding.iso_currency_code = iso_currency_code
            holding.timestamp = datetime.now(tz=timezone.utc)

            session.add(holding)
            session.commit()

            return holding
    return __holding_factory


@pytest.fixture
def holding_balance_factory(db, faker, holding_factory):
    def __holding_balance_factory(
        holding_id=None,
        cost_basis=random.random() * 5,
        quantity=random.randint(1, 500),
    ):
        if holding_id is None:
            holding_id = holding_factory().id

        with db.get_session() as session:
            balance = HoldingBalance()

            balance.id = random.randint(1, 50000)
            balance.holding_id = holding_id
            balance.cost_basis = cost_basis
            balance.quantity = quantity
            balance.timestamp = datetime.now(tz=timezone.utc)

            session.add(balance)
            session.commit()

            return balance
    return __holding_balance_factory


@pytest.fixture
def valid_create_holding_request_factory(account_factory, security_factory):
    def __valid_create_holding_request_factory(
        account_id=None,
        security_symbol=None,
        cost_basis=random.random() * 5,
        quantity=random.randint(1, 500),
        iso_currency_code='USD'
    ):
        if account_id is None:
            account_id = account_factory().id
        if security_symbol is None:
            security_symbol = security_factory().symbol

        return CreateHoldingSchema().load({
            'account_id': account_id,
            'security_symbol': security_symbol,
            'cost_basis': cost_basis,
            'quantity': quantity,
            'iso_currency_code': iso_currency_code,
        })
    return __valid_create_holding_request_factory


@pytest.fixture
def valid_create_holding_balance_request_factory(holding_factory):
    def __valid_create_holding_balance_request_factory(
        holding_id=None,
        cost_basis=random.random() * 5,
        quantity=random.randint(1, 500),
    ):
        if holding_id is None:
            holding_id = holding_factory().id

        return CreateHoldingBalanceSchema().load({
            'holding_id': holding_id,
            'cost_basis': cost_basis,
            'quantity': quantity
        })
    return __valid_create_holding_balance_request_factory


@pytest.fixture
def valid_update_holding_request_factory(holding_factory):
    def __valid_update_holding_request_factory(
        id=None,
        cost_basis=random.random() * 5,
        quantity=random.randint(1, 500),
        iso_currency_code='USD'
    ):
        if id is None:
            id = holding_factory().id

        return UpdateHoldingSchema().load({
            'id': id,
            'cost_basis': cost_basis,
            'quantity': quantity,
            'iso_currency_code': iso_currency_code,
        })
    return __valid_update_holding_request_factory
