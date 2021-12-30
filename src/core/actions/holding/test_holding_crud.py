import pytest

from core.models import Holding, HoldingBalance
from core.schemas.holding_schemas import *
from tests.fixtures import *


def test_cant_create_invalid_create_request():
    assert False


def test_cant_create_invalid_update_request():
    assert False


def test_cant_create_invalid_balance_create_request():
    assert False


def test_get_holding_by_id_returns_holding():
    assert False


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
