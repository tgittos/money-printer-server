import pytest

from core.repositories import RepositoryResponse
from constants import API_PREFIX

from tests.fixtures import *


@pytest.fixture(autouse=True)
def scheduler_spy(mocker):
    return mocker.patch('core.repositories.account_repository.AccountRepository.schedule_account_sync',
        returns=RepositoryResponse(success=True))


@pytest.fixture
def mocked_link_return():
    return {
        'link_token': id_generator(8),
        'request_id': id_generator(8),
        'item_id': id_generator(8),
        'created_at': datetime.now(tz=timezone.utc),
        'expiration': datetime.now(tz=timezone.utc) + timedelta(hours=1),
        'metadata': {}
    }


@pytest.fixture
def mocked_access_return():
    return {
        'access_token': id_generator(8),
        'item_id': id_generator(8),
        'request_id': id_generator(8)
    }


@pytest.fixture(autouse=True)
def plaid_link_spy(mocker, mocked_link_return):
    return mocker.patch('core.apis.plaid.oauth.PlaidOauth.create_link_token',
        return_value=mocked_link_return)


@pytest.fixture(autouse=True)
def plaid_access_spy(mocker, mocked_access_return):
    return mocker.patch('core.apis.plaid.oauth.PlaidOauth.get_access_token',
        return_value=mocked_access_return)


def test_get_plaid_info_returns_plaid_api_info(client, profile_factory, user_token_factory, plaid_item_factory):
    profile = profile_factory()
    item = plaid_item_factory(profile_id=profile.id)
    token = user_token_factory(profile=profile)
    result = client.get(f"/{API_PREFIX}/plaid/info",
        headers={
            'Authorization': f"Bearer {token}"
        })
    assert result.status_code == 200
    json = result.get_json()
    assert json['item_id'] == item.item_id
    assert json['access_token'] == item.access_token


def test_get_plaid_info_returns_empty_fields_with_no_plaid_item(client, user_token_factory):
    token = user_token_factory()
    result = client.get(f"/{API_PREFIX}/plaid/info", headers={
        'Authorization': f"Bearer {token}"
    })
    assert result.status_code == 200
    json = result.get_json()
    assert json['item_id'] is None
    assert json['access_token'] is None

def test_create_link_token_calls_into_plaid_api(client, user_token_factory, plaid_link_spy):
    token = user_token_factory()
    result = client.post(f"/{API_PREFIX}/plaid/link", headers={
        'Authorization': f"Bearer {token}"
    })
    assert result.status_code == 200
    plaid_link_spy.assert_called_once()


def test_create_link_token_returns_plaid_link_token(client, user_token_factory):
    token = user_token_factory()
    result = client.post(f"/{API_PREFIX}/plaid/link", headers={
        'Authorization': f"Bearer {token}"
    })
    assert result.status_code == 200
    json = result.get_json()
    assert json['item_id'] is not None
    assert json['link_token'] is not None


def test_set_access_token_creates_plaid_item(db, client, profile_factory, user_token_factory):
    profile = profile_factory()
    token = user_token_factory(profile=profile)
    with db.get_session() as session:
        old_count = session.query(PlaidItem).where(PlaidItem.profile_id == profile.id).count()
    result = client.post(f"/{API_PREFIX}/plaid/access", headers={
        'Authorization': f"Bearer {token}"
    }, json={
        'public_token': 'foobartoken'
    })
    assert result.status_code == 200
    with db.get_session() as session:
        new_count = session.query(PlaidItem).where(PlaidItem.profile_id == profile.id).count()
    assert new_count == old_count + 1
    


def test_set_access_token_schedules_account_sync(client, user_token_factory, scheduler_spy):
    token = user_token_factory()
    result = client.post(f"/{API_PREFIX}/plaid/access", headers={
        'Authorization': f"Bearer {token}"
    }, json={
        'public_token': id_generator()
    })
    assert result.status_code == 200
    scheduler_spy.assert_called_once()
    


def test_set_access_token_rejects_invalid_token(mocker, client, user_token_factory):
    token = user_token_factory()
    # stub out the oauth api so that it returns an error or an empty object
    mocker.patch('core.apis.plaid.oauth.PlaidOauth.get_access_token',
        return_value=None)
    result = client.post(f"/{API_PREFIX}/plaid/access", headers={
        'Authorization': f"Bearer {token}"
    }, json={
        'public_token': id_generator()
    })
    assert result.status_code == 400