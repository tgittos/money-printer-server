from tests.factories import create_plaid_item
from core.models.plaid_item import PlaidItem
from core.repositories.profile_repository import ProfileRepository

from server.services.api.jobs.sync_accounts import SyncAccounts


def test_sync_accounts_all_accounts_associated_with_plaid_id(mocker):
    job = SyncAccounts({'args': {'plaid_item_id': 'my-plaid-item-id'}})
    mock_plaid_item = PlaidItem()
    mocker.patch.object(job.plaid_repo, 'get_plaid_item_by_id', (lambda _: mock_plaid_item))
    mocker.patch.object(job.profile_repo, 'sync_all_accounts')
    spy = mocker.spy(job.profile_repo, 'sync_all_accounts')
    job.run()
    spy.assert_called_once_with(mock_plaid_item)


def test_sync_accounts_fails_with_no_plaid_id(mocker):
    job = SyncAccounts({ 'args': { 'plaid_item_id': None }})
    spy = mocker.spy(job.profile_repo, 'sync_all_accounts')
    job.run()
    spy.assert_not_called()
