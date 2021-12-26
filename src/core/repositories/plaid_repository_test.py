import pytest

from core.repositories.plaid_repository import PlaidRepository

from tests.fixtures.core import db
from tests.fixtures.plaid_item_fixtures import existing_profile, existing_plaid_item
    
from tests.fixtures.profile_fixtures import profile_with_no_plaids

@pytest.fixture
def repo():
    return PlaidRepository()


@pytest.fixture
def plaid_api_link_spy(mocker):
    return mocker.patch('core.apis.plaid.oauth.PlaidOauth.create_link_token')


@pytest.fixture
def plaid_api_access_spy(mocker):
    return mocker.patch('core.apis.plaid.oauth.PlaidOauth.get_access_token')


def test_info_returns_plaid_item_info_for_profile_when_exists(
    repo, existing_profile, existing_plaid_item):
    result = repo.info(existing_profile.id)
    assert result.success
    assert result.data is not None
    assert result.data['item_id'] == existing_plaid_item.item_id
    assert result.data['access_token'] == existing_plaid_item.access_token


def test_info_fails_when_profile_missing(db, repo):
    result = repo.info(234234)
    assert not result.success
    assert result.data is None


def test_info_fails_with_profile_with_no_plaid_item(repo, profile_with_no_plaids):
    result = repo.info(profile_with_no_plaids.id)
    assert not result.success
    assert result.data is None


def test_create_link_token_calls_into_plaid_api(repo, plaid_api_link_spy):
    result = repo.create_link_token('foobar.com')
    assert result.success
    plaid_api_link_spy.assert_called_once()


def test_get_access_token_calls_into_plaid_api(repo, existing_profile, plaid_api_access_spy):
    result = repo.get_access_token(existing_profile.id, 'foobartoken')
    assert result.success
    plaid_api_access_spy.assert_called_once()


def test_get_access_token_stores_plaid_item(repo, existing_profile):
    assert False