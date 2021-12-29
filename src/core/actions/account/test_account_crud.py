import pytest

from core.models import Account
from core.actions.account.crud import create_account, update_account, get_account_by_id,\
    get_account_by_account_id, get_accounts_by_profile_id, get_accounts_by_plaid_item_id,\
    create_or_update_account
from tests.fixtures import *


def test_create_account_accepts_valid_input(db, plaid_item_factory, valid_create_account_request_factory):
    plaid_item = plaid_item_factory()
    request = valid_create_account_request_factory(profile_id=plaid_item.profile_id, plaid_item_id=plaid_item.id)
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
        num_accounts = session.query(Account).where(Account.profile_id == profile.id).count()
    request = valid_create_account_api_request_factory()
    result = create_or_update_account(db, profile.id, plaid_item.id, request)
    assert result.success
    assert not result.data is None
    assert result.data.name == request['name']
    with db.get_session() as session:
        new_num_accounts = session.query(Account).where(Account.profile_id == profile.id).count()
    assert new_num_accounts == num_accounts + 1


def test_create_or_update_account_updates_account_if_present(db, profile_factory, account_factory,
    valid_update_account_api_request_factory, plaid_item_factory):
    profile = profile_factory()
    plaid_item = plaid_item_factory(profile_id=profile.id)
    account = account_factory(profile_id=profile.id, plaid_item_id=plaid_item.id)
    request = valid_update_account_api_request_factory(profile_id=profile.id, account_account_id=account.account_id)
    with db.get_session() as session:
        num_accounts = session.query(Account).where(Account.profile_id == profile.id).count()
    assert account.name != request['name']
    result = create_or_update_account(db, profile.id, plaid_item.id, request)
    assert result.success
    assert not result.data is None
    assert result.data.name == request['name']
    with db.get_session() as session:
        new_num_accounts = session.query(Account).where(Account.profile_id == profile.id).count()
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

