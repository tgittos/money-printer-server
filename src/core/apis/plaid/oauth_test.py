import pytest
import os

from core.apis.plaid.oauth import PlaidOauth
from core.lib.utilities import id_generator, Struct

from tests.fixtures import *


@pytest.fixture
def repo():
    return PlaidOauth()


def test_create_link_token_calls_plaid_api_link_token_create(mocker, faker, repo, mocked_link_return):
    spy = mocker.patch.object(repo.client, 'link_token_create',
        return_value=Struct(**mocked_link_return))
    repo.create_link_token(faker.domain_name())
    spy.assert_called_once()


def test_create_link_token_uses_env_var_for_webhook_when_set(mocker, faker, repo, mocked_link_return):
    webhook_url = "custom-webhook-host.com"
    host_url = faker.domain_name()
    os.environ['MP_WEBHOOK_HOST'] = webhook_url
    spy = mocker.patch.object(repo.client, 'link_token_create',
        return_value=Struct(**mocked_link_return))
    repo.create_link_token(host_url)
    request = spy.call_args[0][0]
    assert request is not None
    assert request['webhook'] == webhook_url + "/v1/webhooks/plaid"


def test_create_link_token_returns_valid_response(mocker, faker, repo, mocked_link_return):
    mocker.patch.object(repo.client, 'link_token_create',
        return_value=Struct(**mocked_link_return))
    result = repo.create_link_token(faker.domain_name())
    assert result is not None
    assert result == mocked_link_return


def test_get_access_token_calls_plaid_api_item_public_token_exchange(mocker, repo, mocked_access_return):
    spy = mocker.patch.object(repo.client, 'item_public_token_exchange',
        return_value=Struct(**mocked_access_return))
    repo.get_access_token(id_generator())
    spy.assert_called_once()


def test_get_access_token_returns_valid_response(mocker, repo, mocked_access_return):
    mocker.patch.object(repo.client, 'item_public_token_exchange',
        return_value=Struct(**mocked_access_return))
    result = repo.get_access_token(id_generator())
    assert result is not None
    assert result.to_dict() == mocked_access_return
