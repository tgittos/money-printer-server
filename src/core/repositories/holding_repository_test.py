import pytest

from core.repositories import HoldingRepository
from tests.fixtures import *


@pytest.fixture
def repo():
    repo = HoldingRepository()
    return repo


@pytest.fixture
def sync_balances_spy(mocker, repo):
    return mocker.patch.object(repo.security_repo, 'sync_balances')


@pytest.fixture
def sync_transactions_spy(mocker, repo):
    return mocker.patch.object(repo.security_repo, 'sync_transactions')


@pytest.fixture
def instant_job_spy(mocker, repo):
    return mocker.patch.object(repo.scheduled_job_repo, 'create_instant_job')


def test_get_holding_by_id_gets_holding_for_profile(repo, profile_factory, account_factory, holding_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    holding = holding_factory(account_id=account.id)
    result = repo.get_holding_by_id(profile.id, holding.id)
    assert result.success
    assert result.data is not None
    assert result.data.id == holding.id


def test_get_holding_by_id_cant_get_holding_in_another_profile(repo, profile_factory, account_factory, holding_factory):
    profile = profile_factory()
    other_profile = profile_factory()
    other_account = account_factory()
    holding = holding_factory(account_id=other_account.id)
    result = repo.get_holding_by_id(profile.id, holding.id)
    assert not result.success
    assert result.data is None


def test_get_holding_by_id_fails_for_holding_that_doesnt_exist(repo, profile_factory):
    profile = profile_factory()
    result = repo.get_holding_by_id(profile.id, 23423)
    assert not result.success
    assert result.data is None


def test_get_holdings_by_profile_id_gets_holding_for_profile(repo, profile_factory, account_factory,\
    holding_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    holding = holding_factory(account_id=account.id)
    result = repo.get_holdings_by_profile_id(profile.id)
    assert result.success
    assert result.data is not None
    ids = [d.id for d in result.data]
    assert holding.id in ids


def test_get_holdings_by_profile_id_cant_get_holding_in_another_profile(repo, profile_factory, account_factory,\
    holding_factory):
    profile = profile_factory()
    other_profile = profile_factory()
    other_account = account_factory(profile_id=other_profile.id)
    holding = holding_factory(account_id=other_account.id)
    result = repo.get_holdings_by_profile_id(profile.id)
    assert result.success
    assert result.data is not None
    ids = [d.id for d in result.data]
    assert not holding.id in ids


def test_get_holdings_by_profile_id_fails_for_holding_that_doesnt_exist(repo, profile_factory):
    profile = profile_factory()
    result = repo.get_holdings_by_profile_id(profile.id)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 0


def test_get_holding_balances_by_holding_id_gets_holding_for_profile(repo, profile_factory, account_factory,\
    holding_factory, holding_balance_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    holding = holding_factory(account_id=account.id)
    balance = holding_balance_factory(holding_id=holding.id)
    result = repo.get_holding_balances_by_holding_id(profile.id, holding.id)
    assert result.success
    assert result.data is not None
    ids = [d.id for d in result.data]
    assert balance.id in ids


def test_get_holding_balances_by_holding_id_cant_get_holding_in_another_profile(repo, profile_factory,\
    account_factory, holding_factory, holding_balance_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    holding = holding_factory(account_id=account.id)
    balance = holding_balance_factory(holding_id=holding.id)
    result = repo.get_holding_balances_by_holding_id(profile.id, holding.id)
    assert result.success
    assert result.data is not None
    ids = [d.id for d in result.data]
    assert balance.id in ids


def test_get_holding_balances_by_holding_id_fails_for_holding_that_doesnt_exist(repo, profile_factory, account_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    result = repo.get_holding_balances_by_holding_id(profile.id, 23423)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 0


def test_schedule_update_holdings_creates_instant_job(repo, instant_job_spy, plaid_item_factory, profile_factory, account_factory,\
    holding_factory):
    profile = profile_factory()
    item = plaid_item_factory(profile_id=profile.id)
    account = account_factory(profile_id=profile.id, plaid_item_id=item.id)
    holding = holding_factory(account_id=account.id)
    result = repo.schedule_update_holdings(profile.id, item.id)
    assert result.success
    instant_job_spy.assert_called_once()


def test_schedule_update_holdings_fails_for_missing_plaid_item_id(repo, instant_job_spy, profile_factory, account_factory,\
    holding_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    holding = holding_factory(account_id=account.id)
    result = repo.schedule_update_holdings(profile.id, 23423)
    assert not result.success
    assert not instant_job_spy.called


def test_schedule_update_holdings_fails_for_plaid_in_another_profile(repo, profile_factory, plaid_item_factory, account_factory,\
    holding_factory, instant_job_spy):
    profile = profile_factory()
    item = plaid_item_factory()
    account = account_factory(plaid_item_id=item.id)
    holding = holding_factory(account_id=account.id)
    result = repo.schedule_update_holdings(profile.id, item.id)
    assert not result.success
    assert not instant_job_spy.called


def test_schedule_update_transactions_creates_instant_job(repo, instant_job_spy, plaid_item_factory, profile_factory,\
    account_factory, holding_factory):
    profile = profile_factory()
    item = plaid_item_factory(profile_id=profile.id)
    account = account_factory(profile_id=profile.id, plaid_item_id=item.id)
    holding = holding_factory(account_id=account.id)
    result = repo.schedule_update_transactions(profile.id, item.id)
    assert result.success
    instant_job_spy.assert_called_once()


def test_schedule_update_transactions_fails_for_missing_plaid_item_id(repo, profile_factory, instant_job_spy):
    profile = profile_factory()
    result = repo.schedule_update_transactions(profile.id, 234234)
    assert not result.success
    assert not instant_job_spy.called


def test_schedule_update_transactions_fails_for_plaid_in_another_profile(repo, profile_factory, plaid_item_factory,\
    account_factory, holding_factory, instant_job_spy):
    profile = profile_factory()
    item = plaid_item_factory()
    account = account_factory(profile_id = item.profile_id, plaid_item_id=item.id)
    holding = holding_factory(account_id=account.id)
    result = repo.schedule_update_transactions(profile.id, item.id)
    assert not result.success
    assert not instant_job_spy.called


def update_holdings_calls_into_security_repo_for_each_account(repo, sync_balances_spy, profile_factory, plaid_item_factory,\
    account_factory, holding_factory):
    profile = profile_factory()
    item = plaid_item_factory(profile_id=profile.id)
    account = account_factory(profile_id=profile.id, plaid_item_id=item.id)
    holding = holding_factory(account_id=account.id)
    result = repo.update_holdings(profile.id, item.id)
    assert result.success
    sync_balances_spy.assert_called_once()


def update_holdings_fails_for_missing_plaid_item(repo, sync_balances_spy, profile_factory, account_factory, holding_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    holding = holding_factory(account_id=account.id)
    result = repo.update_holdings(profile.id, 23423)
    assert not result.success
    assert not sync_balances_spy.called


def update_holdings_fails_for_plaid_item_in_another_profile(repo, profile_factory, plaid_item_factory, account_factory,\
    holding_factory, sync_balances_spy):
    profile = profile_factory()
    item = plaid_item_factory()
    account = account_factory(account_id=item.account_id, plaid_item_id=item.id)
    holding = holding_factory(account_id=account.id)
    result = repo.update_holdings(profile.id, item.id)
    assert not result.success
    assert not sync_balances_spy.called


def update_transactions_calls_into_security_repo_for_each_account(repo, sync_transactions_spy, account_factory, plaid_item_factory,\
    profile_factory, holding_factory):
    profile = profile_factory()
    item = plaid_item_factory(profile_id=profile.id)
    account = account_factory(profile_id=profile.id, plaid_item_id=item.id)
    holding = holding_factory(account_id=account.id)
    result = repo.update_holdings(profile.id, item.id)
    assert result.success
    sync_transactions_spy.assert_called_once()


def update_transactions_fails_for_missing_plaid_item(repo, profile_factory, account_factory, holding_factory,\
    sync_transactions_spy):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    holding = holding_factory(account_id=account.id)
    result = repo.update_holdings(profile.id, 12312)
    assert not result.success
    assert not sync_transactions_spy.called


def update_transactions_fails_for_plaid_item_in_another_profile(repo, profile_factory, account_factory, holding_factory,\
    sync_transactions_spy):
    profile = profile_factory()
    item = plaid_item_factory()
    account = account_factory(profile_id=profile.id)
    holding = holding_factory(account_id=account.id)
    result = repo.update_holdings(profile.id, item.id)
    assert not result.success
    assert not sync_transactions_spy.called
