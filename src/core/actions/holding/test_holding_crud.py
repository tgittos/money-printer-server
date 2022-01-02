import pytest

from core.models import Holding, HoldingBalance
from core.schemas.holding_schemas import *

from core.actions.holding.holding_crud import *

from tests.fixtures import *


def test_cant_create_invalid_create_request():
    with pytest.raises(Exception):
        CreateHoldingSchema().load({
            'security_symbol': 'AAPL',
            'cost_basis': 200.0,
            'quantity': None
        })


def test_cant_create_invalid_update_request():
    with pytest.raises(Exception):
        UpdateHoldingSchema().load({
            'security_symbol': 'AAPL',
            'cost_basis': 200.0,
            'quantity': None
        })


def test_cant_create_invalid_balance_create_request():
    with pytest.raises(Exception):
        CreateHoldingBalanceSchema().load({
            'cost_basis': 200.0,
            'quantity': None
        })


def test_get_holding_by_id_returns_holding(db, account_factory, valid_create_holding_request_factory):
    account = account_factory()
    request = valid_create_holding_request_factory(account_id=account.id)
    result = create_holding(db, account.id, request)
    assert result.success
    assert result.data is not None
    assert result.data.id is not None


def test_get_holding_by_id_fails_for_missing_holding(db):
    result = get_holding_by_id(db, 24234)
    assert not result.success
    assert result.data is None


def test_get_holdings_by_account_id_returns_holdings_for_account(db, account_factory, holding_factory):
    account = account_factory()
    holding_1 = holding_factory(account_id=account.id)
    holding_2 = holding_factory(account_id=account.id)
    result = get_holdings_by_account_id(db, account_id=account.id)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 2
    ids = [d.id for d in result.data]
    assert holding_1.id in ids
    assert holding_2.id in ids


def test_get_holdings_by_account_id_returns_empty_array_with_no_holdings(db, account_factory):
    account = account_factory()
    result = get_holdings_by_account_id(db, account_id=account.id)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 0


def test_get_holding_balances_by_holding_id_returns_balances(db, holding_factory, holding_balance_factory):
    holding = holding_factory()
    balance_1 = holding_balance_factory(holding_id=holding.id)
    balance_2 = holding_balance_factory(holding_id=holding.id)
    result = get_holding_balances_by_holding_id(db, holding_id=holding.id)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 2
    ids = [d.id for d in result.data]
    assert balance_1.id in ids
    assert balance_2.id in ids


def test_get_holding_balances_by_holding_id_returns_empty_with_no_balances(db, holding_factory):
    holding = holding_factory()
    result = get_holding_balances_by_holding_id(db, holding_id=holding.id)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 0


def test_create_holding_accepts_valid_input(db, account_factory, valid_create_holding_request_factory):
    account = account_factory()
    request = valid_create_holding_request_factory(account_id=account.id)
    with db.get_session() as session:
        pre_count = session.query(Holding).count()
    result = create_holding(db, account.id, request)
    with db.get_session() as session:
        post_count = session.query(Holding).count()
    assert result.success
    assert result.data is not None
    assert result.data.id is not None
    assert post_count == pre_count + 1


def test_update_holding_accepts_valid_input(db, holding_factory, valid_update_holding_request_factory):
    holding = holding_factory()
    request = valid_update_holding_request_factory(id=holding.id)
    assert holding.cost_basis != request['cost_basis']
    result = update_holding(db, request)
    assert result.success
    assert result.data is not None
    assert result.data.id == holding.id
    with db.get_session() as session:
        updated = session.query(Holding).where(
            Holding.id == holding.id).first()
    assert updated.cost_basis == round(request['cost_basis'], 5)


def test_delete_holding_deletes_holding(db, holding_factory):
    holding = holding_factory()
    result = delete_holding(db, holding.id)
    assert result.success
    with db.get_session() as session:
        assert session.query(Holding).where(
            Holding.id == holding.id).first() is None


def test_delete_holding_fails_when_holding_missing(db):
    result = delete_holding(db, 23242342)
    assert not result.success


def test_create_holding_balance_accepts_valid_input(db, holding_factory,
                                                    valid_create_holding_balance_request_factory):
    holding = holding_factory()
    request = valid_create_holding_balance_request_factory(
        holding_id=holding.id)
    with db.get_session() as session:
        balance_count = session.query(HoldingBalance).where(
            HoldingBalance.holding_id == holding.id).count()
        assert balance_count == 0
    result = create_holding_balance(db, request)
    with db.get_session() as session:
        new_balance_count = session.query(HoldingBalance).where(
            HoldingBalance.holding_id == holding.id).count()
        assert new_balance_count == 1
    assert result.success
    assert result.data is not None
    assert result.data.holding_id == holding.id
