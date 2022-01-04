import pytest

from core.repositories import HoldingRepository
from tests.fixtures import *


@pytest.fixture
def repo():
    repo = HoldingRepository()


@pytest.fixture
def sync_balances_spy(mocker, repo):
    return mocker.patch.object(repo.security_repo, 'sync_balances')


@pytest.fixture
def sync_transactions_spy(mocker, repo):
    return mocker.patch.object(repo.security_repo, 'sync_transactions')


def test_get_holding_by_id_gets_holding_for_profile(repo, profile_factory, holding_factory):
    profile = profile_factory()
    holding = holding_factory(profile_id=profile.id)
    result = repo.get_holding_by_id(profile.id, holding.id)
    assert result.success
    assert result.data is not None
    assert result.data.id == holding.id


def test_get_holding_by_id_cant_get_holding_in_another_profile(repo, profile_factory, holding_factory):
    profile = profile_factory()
    holding = holding_factory()
    result = repo.get_holding_by_id(profile.id, holding.id)
    assert not result.success
    assert result.data is None


def test_get_holding_by_id_fails_for_holding_that_doesnt_exist(repo, profile_factory):
    profile = profile_factory()
    result = repo.get_holding_by_id(profile.id, 23423)
    assert not result.success
    assert result.data is None


def test_get_holdings_by_profile_id_gets_holding_for_profile():
    assert False


def test_get_holdings_by_profile_id_cant_get_holding_in_another_profile():
    assert False


def test_get_holdings_by_profile_id_fails_for_holding_that_doesnt_exist():
    assert False


def test_get_holding_balances_by_holding_id_gets_holding_for_profile():
    assert False


def test_get_holding_balances_by_holding_id_cant_get_holding_in_another_profile():
    assert False


def test_get_holding_balances_by_holding_id_fails_for_holding_that_doesnt_exist():
    assert False


def test_schedule_update_holdings_creates_instant_job():
    assert False


def test_schedule_update_holdings_fails_for_missing_plaid_item_id():
    assert False


def test_schedule_update_holdings_fails_for_plaid_in_another_profile():
    assert False


def test_schedule_update_transactions_creates_instant_job():
    assert False


def test_schedule_update_transactions_fails_for_missing_plaid_item_id():
    assert False


def test_schedule_update_transactions_fails_for_plaid_in_another_profile():
    assert False


def update_holdings_calls_into_security_repo_for_each_account():
    assert False


def update_holdings_fails_for_missing_plaid_item():
    assert False


def update_holdings_fails_for_plaid_item_in_another_profile():
    assert False


def update_transactions_calls_into_security_repo_for_each_account():
    assert False


def update_transactions_fails_for_missing_plaid_item():
    assert False


def update_transactions_fails_for_plaid_item_in_another_profile():
    assert False
