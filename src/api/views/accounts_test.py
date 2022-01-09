import pytest

from constants import API_PREFIX

from tests.fixtures import *


def test_list_accounts_returns_all_accounts_for_profile(client, profile_factory,
    account_factory, user_token_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    token = user_token_factory(profile=profile)
    response = client.get(f"/{API_PREFIX}/accounts/", headers={
        'Authorization': f"Bearer {token}"
    })
    assert response.status_code == 200
    result = response.get_json()
    assert result is not None
    assert result['success']
    assert len(result['data']) == 1
    assert result['data'][0]['id'] == account.id


def test_list_accounts_returns_no_accounts(client, user_token_factory):
    token = user_token_factory()
    response = client.get(f"/{API_PREFIX}/accounts/", headers={
        'Authorization': f"Bearer {token}"
    })
    assert response.status_code == 200
    result = response.get_json()
    assert result is not None
    assert result['success']
    assert len(result['data']) == 0


def test_list_accounts_fails_for_no_token(client):
    response = client.get(f"/{API_PREFIX}/accounts/")
    assert response.status_code == 401


def test_request_account_sync_schedules_instant_job(mocker, client, profile_factory, account_factory,
    user_token_factory):
    spy = mocker.patch('core.repositories.account_repository.AccountRepository.schedule_account_sync')
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    token = user_token_factory(profile=profile)
    response = client.post(f"/{API_PREFIX}/accounts/{account.id}/sync",
        headers={
            'Authorization': f"Bearer {token}"
        })
    assert response.status_code == 200
    spy.assert_called_once()


def test_request_account_sync_fails_with_no_profile(client, profile_factory, account_factory, user_token_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    token = user_token_factory(profile=profile)
    response = client.post(f"/{API_PREFIX}/accounts/23423/sync",
        headers={
            'Authorization': f"Bearer {token}"
        })
    assert response.status_code == 400


def test_request_account_sync_fails_with_no_token(client, profile_factory, account_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    response = client.post(f"/{API_PREFIX}/accounts/{account.id}/sync")
    assert response.status_code == 401


def test_request_account_balances_returns_balances(client, user_token_factory,
    profile_factory, account_factory, account_balance_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    balance = account_balance_factory(account_id=account.id)
    token = user_token_factory(profile=profile)
    response = client.get(f"/{API_PREFIX}/accounts/{account.id}/balances",
        headers={
            'Authorization': f"Bearer {token}"
        })
    assert response.status_code == 200
    result = response.get_json()
    assert result is not None
    assert result['success']
    assert len(result['data']) == 1
    assert result['data'][0]['id'] == balance.id


def test_request_account_balances_fails_with_no_account(client, user_token_factory,
    profile_factory, account_factory, account_balance_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    balance = account_balance_factory(account_id=account.id)
    token = user_token_factory(profile=profile)
    response = client.get(f"/{API_PREFIX}/accounts/234242/balances",
        headers={
            'Authorization': f"Bearer {token}"
        })
    assert response.status_code == 200
    result = response.get_json()
    assert result is not None
    assert result['success']
    assert len(result['data']) == 0


def test_request_account_balances_fails_with_no_token(client, user_token_factory,
    profile_factory, account_factory, account_balance_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    balance = account_balance_factory(account_id=account.id)
    token = user_token_factory(profile=profile)
    response = client.get(f"/{API_PREFIX}/accounts/{account.id}/balances")
    assert response.status_code == 401


def test_request_holdings_gets_holdings_for_account(client, user_token_factory,
    profile_factory, account_factory, holding_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    holding = holding_factory(account_id=account.id)
    token = user_token_factory(profile=profile)
    response = client.get(f"/{API_PREFIX}/accounts/{account.id}/holdings",
        headers={
            'Authorization': f"Bearer {token}"
        })
    assert response.status_code == 200
    result = response.get_json() 
    assert result is not None
    assert result['success']
    assert result['data'] is not None
    assert len(result['data']) == 1
    assert result['data'][0]['id'] == holding.id


def test_request_holdings_fails_for_no_account(client, user_token_factory,
    profile_factory, account_factory, holding_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    holding = holding_factory(account_id=account.id)
    token = user_token_factory(profile=profile)
    response = client.get(f"/{API_PREFIX}/accounts/23423452/holdings",
        headers={
            'Authorization': f"Bearer {token}"
        })
    assert response.status_code == 404


def test_request_holdings_fails_for_no_token(client, user_token_factory,
    profile_factory, account_factory, account_balance_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    balance = account_balance_factory(account_id=account.id)
    token = user_token_factory(profile=profile)
    response = client.get(f"/{API_PREFIX}/accounts/{account.id}/holdings")
    assert response.status_code == 401
