import pytest
from datetime import datetime, timezone, timedelta

from core.actions.balance.crud import create_account_balance, get_balances_by_account, get_latest_balance_by_account
from core.models import AccountBalance

from tests.fixtures import *


def test_create_account_balance_accepts_valid_input(db, valid_create_account_balance_request_factory):
    with db.get_session() as session:
        old_count = session.query(AccountBalance).count()
    request = valid_create_account_balance_request_factory()
    result = create_account_balance(db, request)
    assert result.success
    assert result.data is not None
    with db.get_session() as session:
        new_count = session.query(AccountBalance).count()
    assert new_count == old_count + 1


def test_get_balances_by_account_obeys_start_and_end(db, account_factory, account_balance_factory):
    account = account_factory()
    balance_before_window = account_balance_factory(
        account_id=account.id,
        timestamp=datetime.now(tz=timezone.utc) - timedelta(days=45))
    balance_inside_start = account_balance_factory(
        account_id=account.id,
        timestamp=datetime.now(tz=timezone.utc) - timedelta(days=25))
    balance_after_start = account_balance_factory(
        account_id=account.id,
        timestamp=datetime.now(tz=timezone.utc))
    start = datetime.now(tz=timezone.utc) - timedelta(days=30)
    end = datetime.now(tz=timezone.utc) - timedelta(days=1)
    result = get_balances_by_account(db, account.id, start, end)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 1
    assert result.data[0].id == balance_inside_start.id


def test_get_balances_by_account_gets_all_since_start_if_end_omitted(db, account_factory, account_balance_factory):
    account = account_factory()
    balance_before_window = account_balance_factory(
        account_id=account.id,
        timestamp=datetime.now(tz=timezone.utc) - timedelta(days=45))
    balance_inside_start = account_balance_factory(
        account_id=account.id,
        timestamp=datetime.now(tz=timezone.utc) - timedelta(days=25))
    balance_after_start = account_balance_factory(
        account_id=account.id,
        timestamp=datetime.now(tz=timezone.utc))
    end = datetime.now(tz=timezone.utc) - timedelta(days=10)
    result = get_balances_by_account(db, account.id, end=end)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 2
    assert result.data[0].id == balance_before_window.id
    assert result.data[1].id == balance_inside_start.id


def test_get_balances_by_account_gets_all_if_start_and_end_omitted(db, account_factory, account_balance_factory):
    account = account_factory()
    balance_before_window = account_balance_factory(
        account_id=account.id,
        timestamp=datetime.now(tz=timezone.utc) - timedelta(days=45))
    balance_inside_start = account_balance_factory(
        account_id=account.id,
        timestamp=datetime.now(tz=timezone.utc) - timedelta(days=25))
    balance_after_start = account_balance_factory(
        account_id=account.id,
        timestamp=datetime.now(tz=timezone.utc))
    end = datetime.now(tz=timezone.utc) - timedelta(days=1)
    result = get_balances_by_account(db, account.id)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 3


def test_get_balances_by_account_returns_empty_list_if_none_found(db, account_factory):
    account = account_factory()
    result = get_balances_by_account(db, account.id)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 0


def test_get_latest_balance_by_account_returns_latest_balance(db, account_factory, account_balance_factory):
    account = account_factory()
    older_balance = account_balance_factory(
        account_id=account.id,
        timestamp=datetime.now(tz=timezone.utc) - timedelta(days=45))
    newer_balance = account_balance_factory(
        account_id=account.id,
        timestamp=datetime.now(tz=timezone.utc))
    result = get_latest_balance_by_account(db, account.id)
    assert result.success
    assert result.data is not None
    assert result.data.id == newer_balance.id


def test_get_latest_balance_by_account_fails_if_no_balances_available(db, account_factory):
    account = account_factory()
    result = get_latest_balance_by_account(db, account.id)
    assert not result.success
    assert result.data is None
