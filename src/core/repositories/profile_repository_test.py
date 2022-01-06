import pytest

import core.repositories.profile_repository as profile_repo_module
from core.repositories.profile_repository import ProfileRepository
from core.repositories.repository_response import RepositoryResponse

from tests.fixtures import *


@pytest.fixture(autouse=True)
def repository(db, mocker):
    repo = ProfileRepository()
    fake_job_repo = mocker.patch.object(
        repo, 'scheduled_job_repo', autospec=True)
    mock_repo = mocker.Mock()
    mock_repo.create_instant_job.return_value = RepositoryResponse(
        success=True
    )
    fake_job_repo.side_effect = mock_repo
    fake_job_repo.create_instant_job.__name__ = "create_instant_job_mocked"
    return repo


@pytest.fixture()
def instant_job_spy(mocker, repository):
    instant_job_spy = mocker.spy(
        repository.scheduled_job_repo, 'create_instant_job')
    return instant_job_spy


def test_schedule_profile_sync_creates_instant_job(repository, profile_factory, plaid_item_factory, instant_job_spy):
    profile = profile_factory()
    item = plaid_item_factory(profile_id=profile.id)
    result = repository.schedule_profile_sync(profile.id)
    assert result.success
    assert instant_job_spy.assert_called_once()


def test_schedule_profile_sync_fails_with_invalid_profile_id(repository):
    result = repository.schedule_profile_sync(2342)
    assert not result.success
    assert result.data is None


def test_schedule_profile_sync_fails_with_no_plaid_items_for_profile(repository, profile_factory):
    profile = profile_factory()
    result = repository.schedule_profile_sync(profile.id)
    assert not result.success
    assert result.data is None


def test_sync_all_accounts_requests_accounts_from_plaid(mocker, repository, plaid_item_factory):
    item = plaid_item_factory()
    # mock dependencies not under test
    mocker.patch.object(repository.account_repo, 'sync_account_balance')
    mocker.patch.object(repository.holdings_repo, 'update_holdings')
    # ensure we request from plaid
    spy = mocker.patch.object(repository.plaid_accounts_api, 'get_accounts')
    result = repository.sync_all_accounts(item.profile_id, item.id)
    assert result.success
    spy.assert_called_once()


def test_sync_all_accounts_calls_create_or_update_account(db, mocker, plaid_item_factory, repository):
    item = plaid_item_factory()
    # mock dependencies not under test
    mocker.patch.object(repository.account_repo, 'sync_account_balance')
    mocker.patch.object(repository.holdings_repo, 'update_holdings')
    mocker.patch.object(repository.plaid_accounts_api, 'get_accounts', return_value={
        'accounts': [{
            'account_id': 'foobar'
        }]
    })
    # ensure we try to create_or_update_account
    # this method is tested in the actions test
    spy = mocker.patch(
        'core.repositories.profile_repository.create_or_update_account')
    # do the test
    result = repository.sync_all_accounts(item.profile_id, item.id)
    assert result.success
    spy.assert_called_once()


def test_sync_all_accounts_syncs_balances_for_accounts(mocker, repository, profile_factory, plaid_item_factory):
    profile = profile_factory()
    item = plaid_item_factory(profile_id=profile.id)
    # mock dependencies not under test
    mocker.patch.object(repository.holdings_repo, 'update_holdings')
    mocker.patch.object(repository.plaid_accounts_api, 'get_accounts', return_value={
        'accounts': [{
            'account_id': 'foobar'
        }]
    })
    mocker.patch(
        'core.repositories.profile_repository.create_or_update_account')
    # ensure we try to create_or_update_account
    # this method is tested in the actions test
    spy = mocker.patch.object(repository.account_repo, 'sync_account_balance')
    # do the test
    result = repository.sync_all_accounts(profile.id, item.id)
    assert result.success
    spy.assert_called_once()


def test_sync_all_accounts_updates_holdings(mocker, repository, plaid_item_factory):
    item = plaid_item_factory()
    # mock dependencies not under test
    mocker.patch.object(repository.account_repo, 'sync_account_balance')
    mocker.patch.object(repository.plaid_accounts_api, 'get_accounts')
    mocker.patch(
        'core.repositories.profile_repository.create_or_update_account')
    # ensure we try to create_or_update_account
    # this method is tested in the actions test
    spy = mocker.patch.object(repository.holdings_repo, 'update_holdings')
    # do the test
    result = repository.sync_all_accounts(item.profile_id, item.id)
    assert result.success
    spy.assert_called_once()


def test_sync_all_accounts_fails_with_invalid_plaid_item_id(repository, profile_factory):
    profile = profile_factory()
    result = repository.sync_all_accounts(profile.id, 2342)
    assert not result.success
    assert result.data is None
