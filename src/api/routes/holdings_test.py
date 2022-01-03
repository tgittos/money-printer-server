import pytest

from core.models import Holding
from api.lib.constants import API_PREFIX

from tests.fixtures import *


def test_get_holdings_by_profile_id_returns_holdings(
        client, profile_factory, user_token_factory, holding_factory,
        account_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    holding = holding_factory(account_id=account.id)
    token = user_token_factory(profile=profile)
    response = client.get(f"/{API_PREFIX}/holdings",
                          headers={
                              'Authorization': f"Bearer {token}"
                          })
    assert response.status_code == 200
    result = response.get_json()
    assert result is not None
    assert result['success']
    assert result['data'] is not None
    assert holding.id in [d['id'] for d in result['data']]


def test_get_holdings_by_profile_id_returns_empty_array_with_no_holdings(
        db, client, profile_factory, account_factory, user_token_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    token = user_token_factory(profile=profile)
    response = client.get(f"/{API_PREFIX}/holdings",
                          headers={
                              'Authorization': f"Bearer {token}"
                          })
    assert response.status_code == 200
    result = response.get_json()
    assert result is not None
    assert result['success']
    assert result['data'] is not None
    assert len(result['data']) == 0


def test_get_holdings_by_profile_id_fails_unauthed(client, profile_factory):
    profile = profile_factory()
    response = client.get(f"/{API_PREFIX}/holdings")
    assert response.status_code == 401


def test_get_holding_by_id_returns_holding(
        client, profile_factory, account_factory, holding_factory, user_token_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    holding = holding_factory(account_id=account.id)
    token = user_token_factory(profile=profile)
    response = client.get(f"/{API_PREFIX}/holdings/{holding.id}",
                          headers={
                              'Authorization': f"Bearer {token}"
                          })
    assert response.status_code == 200
    result = response.get_json()
    assert result is not None
    assert result['success']
    assert result['data'] is not None
    assert result['data']['id'] == holding.id


def test_get_holding_by_id_returns_404_with_missing_holding(client, user_token_factory):
    token = user_token_factory()
    response = client.get(f"/{API_PREFIX}/holdings/23423423",
                          headers={
                              'Authorization': f"Bearer {token}"
                          })
    assert response.status_code == 404


def test_get_holding_details_fails_when_unauthenticated(
        client, account_factory, holding_factory):
    account = account_factory()
    holding = holding_factory()
    response = client.get(f"/{API_PREFIX}/holdings/{holding.id}")
    assert response.status_code == 401


def test_get_holding_balances_returns_balances_for_holding(
        client, profile_factory, account_factory, holding_factory, holding_balance_factory,
        user_token_factory):
    profile = profile_factory()
    account = account_factory(profile_id=profile.id)
    holding = holding_factory(account_id=account.id)
    balance = holding_balance_factory(holding_id=holding.id)
    token = user_token_factory(profile=profile)
    response = client.get(f"/{API_PREFIX}/holdings/{holding.id}/balances",
                          headers={
                              'Authorization': f"Bearer {token}"
                          })
    assert response.status_code == 200
    result = response.get_json()
    assert result is not None
    assert result['success']
    assert result['data'] is not None
    assert balance.id in [d['id'] for d in result['data']]
