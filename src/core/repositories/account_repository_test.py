import pytest

from core.repositories import AccountRepository

from tests.fixtures import *


@pytest.fixture
def repo():
    return AccountRepository()


def test_get_accounts_by_profile_id_returns_accounts_for_profile(
    repo, profile_factory, account_factory):
    profile = profile_factory()
    account_1 = account_factory(profile_id=profile.id)
    account_2 = account_factory(profile_id=profile.id)
    result = repo.get_accounts_by_profile_id(profile.id)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 2
    assert result.data[0].id == account_1.id
    assert result.data[1].id == account_2.id


def test_get_accounts_fails_when_profile_has_no_accounts(
    repo, profile_factory):
    profile = profile_factory()
    result = repo.get_accounts_by_profile_id(profile.id)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 0


def test_get_accounts_fails_with_no_profile(repo):
    result = repo.get_accounts_by_profile_id(23423)
    assert result.success
    assert len(result.data) == 0


def test_get_accounts_by_profile_with_balances_returns_latest_balances():
    assert False


def test_get_accounts_by_profile_with_balances_ignores_old_balances():
    assert False


def test_get_accounts_by_profile_with_balances_fails_with_no_profile(repo):
    result = repo.get_accounts_by_profile_with_balances(2342)
    assert not result.success
    assert result.data is None


def test_get_account_by_profile_with_balances_returns_latest_balances():
    assert False


def test_get_account_by_profile_with_balances_ignores_old_balances():
    assert False


def test_get_account_by_profile_with_balances_fails_with_no_profile(repo):
    result = repo.get_account_by_profile_with_balance(23423, 234234)
    assert not result.success
    assert result.data is None


def test_schedlue_account_sync_creates_instant_job(mocker, repo, profile_factory, account_factory):
    spy = mocker.patch.object(repo.scheduled_job_repo, 'create_instant_job')
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    result = repo.schedule_account_sync(profile.id, account.id)
    assert result.success
    spy.assert_called_once()


def test_schedule_account_sync_fails_with_no_account(repo, profile_factory):
    profile = profile_factory()
    result = repo.schedule_account_sync(profile.id, 23423)
    assert not result.success
    assert result.data is None


def test_schedule_update_all_balances_schedules_instant_job(mocker, repo, plaid_item_factory):
    spy = mocker.patch.object(repo.scheduled_job_repo, 'create_instant_job')
    item = plaid_item_factory()
    result = repo.schedule_update_all_balances(item.id)
    spy.assert_called_once()


def test_schedule_update_all_balances_fails_with_no_plaid_item(repo):
    result = repo.schedule_update_all_balances(23423)
    assert not result.success
    assert result.data is None


def test_schedule_update_balance_schedules_instant_job(mocker, repo, account_factory):
    spy = mocker.patch.object(repo.scheduled_job_repo, 'create_instant_job')
    account = account_factory()
    result = repo.schedule_update_balance(account.profile_id, account.id)
    assert result.success
    spy.assert_called_once()


def test_schedule_update_balance_fails_with_no_account(repo, profile_factory):
    profile = profile_factory()
    result = repo.schedule_update_balance(profile.id, 2423)
    assert not result.success
    assert result.data is None


def test_sync_all_balances_calls_into_plaid_api_for_each_account():
    assert False


def test_sync_all_balances_fails_for_no_plaid_item(repo):
    result = repo.sync_all_balances(2342)
    assert not result.success
    assert result.data is None


def test_sync_account_balance_calls_into_plaid_api():
    assert False


def test_sync_account_balance_fails_for_no_accounts():
    assert False


def test_sync_account_balance_creates_new_balance_record():
    assert False
