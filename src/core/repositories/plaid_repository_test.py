import pytest
from faker.providers import internet
from datetime import datetime, timezone, timedelta

from core.repositories.plaid_repository import PlaidRepository
from core.lib.utilities import id_generator

from tests.fixtures import *



@pytest.fixture
def repo():
    return PlaidRepository()


@pytest.fixture
def plaid_api_link_spy(mocker, valid_plaid_item_create_request_factory, mocked_link_return):
    request = valid_plaid_item_create_request_factory()
    return mocker.patch('core.apis.plaid.oauth.PlaidOauth.create_link_token', return_value=mocked_link_return)


@pytest.fixture
def plaid_api_access_spy(mocker, valid_plaid_item_create_request_factory, mocked_access_return):
    request = valid_plaid_item_create_request_factory()
    return mocker.patch('core.apis.plaid.oauth.PlaidOauth.get_access_token', return_value=mocked_access_return)


def test_info_returns_plaid_item_info_for_profile_when_exists(
        repo, profile_factory, plaid_item_factory):
    profile = profile_factory()
    item = plaid_item_factory(profile_id=profile.id)
    result = repo.info(profile.id)
    assert result.success
    assert result.data is not None
    assert result.data['item_id'] == item.item_id
    assert result.data['access_token'] == item.access_token


def test_info_fails_when_profile_missing(db, repo):
    result = repo.info(234234)
    assert not result.success
    assert result.data is None


def test_info_fails_with_profile_with_no_plaid_item(repo, profile_factory):
    profile = profile_factory()
    result = repo.info(profile.id)
    assert not result.success
    assert result.data is None


def test_create_link_token_calls_into_plaid_api(repo, profile_factory, faker, plaid_api_link_spy):
    profile = profile_factory()
    faker.add_provider(internet)
    result = repo.create_link_token(profile.id, faker.domain_name())
    assert result.success
    plaid_api_link_spy.assert_called_once()


def test_get_access_token_calls_into_plaid_api(repo, profile_factory, plaid_api_access_spy):
    profile = profile_factory()
    result = repo.get_access_token(profile.id, id_generator())
    assert result.success
    plaid_api_access_spy.assert_called_once()


def test_get_access_token_stores_plaid_item(db, repo, profile_factory, plaid_api_access_spy):
    profile = profile_factory()
    with db.get_session() as session:
        old_count = session.query(PlaidItem).where(PlaidItem.profile_id == profile.id).count()
    result = repo.get_access_token(profile.id, id_generator())
    with db.get_session() as session:
        new_count = session.query(PlaidItem).where(PlaidItem.profile_id == profile.id).count()
    assert new_count == old_count + 1

