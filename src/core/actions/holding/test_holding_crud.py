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


def test_get_holding_by_id_fails_for_missing_holding():
    assert False


def test_get_holdings_by_account_id_returns_holdings_for_account():
    assert False


def test_get_holdings_by_account_id_returns_empty_array_with_no_holdings():
    assert False


def test_get_holding_balances_by_holding_id_returns_balances():
    assert False


def test_get_holding_balances_by_holding_id_returns_empty_with_no_balances():
    assert False


def test_create_holding_accepts_valid_input():
    assert False


def test_update_holding_accepts_valid_input():
    assert False


def test_delete_holding_deletes_holding():
    assert False


def test_delete_holding_fails_when_holding_missing():
    assert False


def test_create_holding_balance_accepts_valid_input():
    assert False
