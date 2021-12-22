import pytest

from core.repositories.profile_repository import ProfileRepository
from core.repositories.repository_response import RepositoryResponse

from tests.factories import create_user_profile, create_plaid_item
from tests.helpers import db


@pytest.fixture(autouse=True)
def profile(db):
    with db.get_session() as session:
        return create_user_profile(session)


@pytest.fixture(autouse=True)
def plaid_item_with_profile(db, profile):
    with db.get_session() as session:
        return create_plaid_item(session, profile_id=profile.id)


@pytest.fixture(autouse=True)
def repository(mocker):
    repo = ProfileRepository()
    fake_job_repo = mocker.patch.object(repo, 'scheduled_job_repo', autospec=True)
    mock_repo = mocker.Mock()
    mock_repo.create_instant_job.return_value = RepositoryResponse(
        success=True
    )
    fake_job_repo.side_effect = mock_repo
    fake_job_repo.create_instant_job.__name__ = "create_instant_job_mocked"
    return repo


@pytest.fixture()
def instant_job_spy(mocker, repository):
    instant_job_spy = mocker.spy(repository.scheduled_job_repo, 'create_instant_job')
    return instant_job_spy


@pytest.fixture()
def profile_with_no_plaids(db):
    with db.get_session() as session:
        return create_user_profile(session)


def test_schedule_profile_sync_creates_instant_job(repository, profile, instant_job_spy):
    result = repository.schedule_profile_sync(profile.id)
    assert result.success
    assert instant_job_spy.assert_called_once()


def test_schedule_profile_sync_fails_with_invalid_profile_id(repository):
    result = repository.schedule_profile_sync(2342)
    assert not result.success
    assert result.data is None


def test_schedule_profile_sync_fails_with_no_plaid_items_for_profile(repository, profile_with_no_plaids):
    result = repository.schedule_profile_sync(profile_with_no_plaids.id)
    assert not result.success
    assert result.data is None


def test_sync_all_accounts_requests_accounts_from_plaid():
    assert False


def test_sync_all_accounts_creates_new_accounts_when_missing():
    assert False


def test_sync_all_accounts_updates_existing_account():
    assert False


def test_sync_all_accounts_syncs_balances_for_accounts():
    assert False


def test_sync_all_accounts_updates_holdings():
    assert False


def test_sync_all_accounts_fails_with_invalid_plaid_item_id():
    assert False


def test_sync_all_accounts_fails_with_orphaned_plaid_item():
    assert False
