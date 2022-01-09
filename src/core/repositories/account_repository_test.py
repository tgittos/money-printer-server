import pytest

from core.repositories import AccountRepository
from core.models import AccountBalance

from tests.fixtures import *


@pytest.fixture
def repo(db):
    return AccountRepository(db)


@pytest.fixture
def plaid_api_response(valid_update_account_api_request_factory,
    valid_create_account_balance_api_request_factory):
    account_dict = valid_update_account_api_request_factory()
    balance_dict = valid_create_account_balance_api_request_factory(account_id=account_dict['id'])
    account_dict['balances'] = balance_dict
    return {
        'accounts': [ account_dict ]
    }


def test_get_accounts_by_profile_id_returns_accounts_for_profile(
    repo, profile_factory, account_factory):
    profile = profile_factory()
    account_1 = account_factory(profile_id=profile.id)
    account_2 = account_factory(profile_id=profile.id)
    result = repo.get_accounts_by_profile_id(profile.id)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 2
    ids = [d.id for d in result.data]
    assert account_1.id in ids
    assert account_2.id in ids


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
    result = repo.schedule_update_all_balances(item.profile_id, item.id)
    spy.assert_called_once()


def test_schedule_update_all_balances_fails_with_no_plaid_item(repo, profile_factory):
    profile = profile_factory()
    result = repo.schedule_update_all_balances(profile.id, 23423)
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


def test_sync_all_balances_calls_into_plaid_api_for_each_account(mocker, repo, plaid_item_factory,
    account_factory, plaid_api_response):
    spy = mocker.patch.object(repo.plaid_accounts_api, 'get_account_balance',
        return_value=plaid_api_response)
    item = plaid_item_factory()
    account_factory(profile_id=item.profile_id)
    account_factory(profile_id=item.profile_id)
    account_factory(profile_id=item.profile_id)
    result = repo.sync_all_balances(item.profile_id, item.id)
    spy.call_count == 3


def test_sync_all_balances_fails_for_no_plaid_item(repo, profile_factory):
    profile = profile_factory()
    result = repo.sync_all_balances(profile.id, 2342)
    assert not result.success
    assert result.data is None


def test_sync_account_balance_calls_into_plaid_api(mocker, repo, profile_factory,
    account_factory, plaid_api_response):
    spy = mocker.patch.object(repo.plaid_accounts_api, 'get_account_balance',
        return_value=plaid_api_response)
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    result = repo.sync_account_balance(profile.id, account.id)
    assert result.success
    spy.assert_called_once()


def test_sync_account_balance_fails_for_no_accounts(repo):
    result = repo.sync_account_balance(2342, 23423)
    assert not result.success
    assert result.data is None


def test_sync_account_balance_creates_new_balance_record(db, mocker, repo, profile_factory,
    account_factory, plaid_api_response):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    plaid_api_response['accounts'][0]['account_id'] = account.account_id
    plaid_api_response['accounts'][0]['balances']['account_id'] = account.id
    spy = mocker.patch.object(repo.plaid_accounts_api, 'get_account_balance',
        return_value=plaid_api_response)
    with db.get_session() as session:
        old_balance_count = session.query(AccountBalance).where(
            AccountBalance.account_id == account.id).count() 
    result = repo.sync_account_balance(profile.id, account.id)
    with db.get_session() as session:
        new_balance_count = session.query(AccountBalance).where(
            AccountBalance.account_id == account.id).count() 
    assert result.success
    assert new_balance_count == old_balance_count + 1
