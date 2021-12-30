import pytest

from core.models import Account
from core.actions.account.crud import *
from tests.fixtures import *


def test_create_account_accepts_valid_input(db, plaid_item_factory, valid_create_account_request_factory):
    plaid_item = plaid_item_factory()
    request = valid_create_account_request_factory(
        profile_id=plaid_item.profile_id, plaid_item_id=plaid_item.id)
    result = create_account(db, plaid_item.profile_id, plaid_item.id, request)
    assert result.success
    assert result.data is not None
    assert result.data.id is not None


def test_update_account_accepts_valid_input(db, profile_factory, account_factory, valid_update_account_request_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    request = valid_update_account_request_factory(
        account_id=account.id, profile_id=profile.id)
    assert account.name != request['name']
    result = update_account(db, profile.id, request)
    assert result.success
    assert result.data is not None
    assert result.data.name == request['name']


def test_create_or_update_account_creates_account_if_missing(db, profile_factory, plaid_item_factory, valid_create_account_api_request_factory):
    profile = profile_factory()
    plaid_item = plaid_item_factory(profile_id=profile.id)
    with db.get_session() as session:
        num_accounts = session.query(Account).where(
            Account.profile_id == profile.id).count()
    request = valid_create_account_api_request_factory()
    result = create_or_update_account(db, profile.id, plaid_item.id, request)
    assert result.success
    assert not result.data is None
    assert result.data.name == request['name']
    with db.get_session() as session:
        new_num_accounts = session.query(Account).where(
            Account.profile_id == profile.id).count()
    assert new_num_accounts == num_accounts + 1


def test_create_or_update_account_updates_account_if_present(db, profile_factory, account_factory,
                                                             valid_update_account_api_request_factory, plaid_item_factory):
    profile = profile_factory()
    plaid_item = plaid_item_factory(profile_id=profile.id)
    account = account_factory(profile_id=profile.id,
                              plaid_item_id=plaid_item.id)
    request = valid_update_account_api_request_factory(
        profile_id=profile.id, account_account_id=account.account_id)
    with db.get_session() as session:
        num_accounts = session.query(Account).where(
            Account.profile_id == profile.id).count()
    assert account.name != request['name']
    result = create_or_update_account(db, profile.id, plaid_item.id, request)
    assert result.success
    assert not result.data is None
    assert result.data.name == request['name']
    with db.get_session() as session:
        new_num_accounts = session.query(Account).where(
            Account.profile_id == profile.id).count()
    assert new_num_accounts == num_accounts


def test_get_account_by_id_returns_account(db, profile_factory, account_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    result = get_account_by_id(db, profile.id, account.id)
    assert result.success
    assert result.data is not None
    assert result.data.id == account.id


def test_get_account_id_fails_for_missing_account(db, profile_factory):
    profile = profile_factory()
    result = get_account_by_id(db, profile.id, 234232)
    assert not result.success
    assert result.data is None


def test_get_account_by_account_id_returns_account(db, profile_factory, account_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    result = get_account_by_account_id(db, profile.id, account.account_id)
    assert result.success
    assert result.data is not None
    assert result.data.id == account.id


def test_get_account_account_id_fails_for_missing_account(db, profile_factory):
    profile = profile_factory()
    result = get_account_by_account_id(db, profile.id, '2lkjl232323l')
    assert not result.success
    assert result.data is None


def test_get_account_by_profile_returns_account(db, profile_factory, account_factory):
    profile = profile_factory()
    account_1 = account_factory(profile_id=profile.id)
    account_2 = account_factory(profile_id=profile.id)
    result = get_accounts_by_profile_id(db, profile.id)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 2


def test_get_account_profile_fails_for_missing_account(db, profile_factory):
    profile = profile_factory()
    result = get_accounts_by_profile_id(db, profile.id)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 0


def test_get_account_by_plaid_item_returns_account(db, plaid_item_factory, account_factory):
    item = plaid_item_factory()
    account = account_factory(plaid_item_id=item.id)
    result = get_accounts_by_plaid_item_id(db, item.id)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 1


def test_get_account_plaid_item_fails_for_missing_account(db, plaid_item_factory):
    item = plaid_item_factory()
    result = get_accounts_by_plaid_item_id(db, item.id)
    assert result.success
    assert len(result.data) == 0


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
