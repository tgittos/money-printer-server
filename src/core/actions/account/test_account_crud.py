import pytest

from core.actions.account.crud import create_account, update_account, get_account_by_id,\
    get_account_by_account_id, get_accounts_by_profile_id
from tests.fixtures import *


def test_create_account_accepts_valid_input(db, valid_create_account_request_factory):
    request = valid_create_account_request_factory()
    result = create_account(db, request)
    assert result.success
    assert result.data is not None
    assert result.data.id is not None


def test_update_account_accepts_valid_input(db, profile_factory, account_factory, valid_update_account_request_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    request = valid_update_account_request_factory(
        account_id=account.id, profile_id=profile.id)
    assert account.name != request['name']
    result = update_account(db, request)
    assert result.success
    assert result.data is not None
    assert result.data.name == request['name']


def test_create_or_update_account_creates_account_if_missing():
    assert False


def test_create_or_update_account_updates_account_if_present():
    assert False


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


def test_get_account_by_plaid_item_returns_account():
    assert False


def test_get_account_plaid_item_fails_for_missing_account():
    assert False
