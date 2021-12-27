import pytest
from marshmallow import ValidationError

from core.schemas.plaid_item_schemas import CreatePlaidItemSchema, UpdatePlaidItemSchema
from core.actions.plaid.crud import *
from core.lib.utilities import id_generator

from tests.fixtures.core import db, factory
from tests.fixtures.profile_fixtures import profile_factory
from tests.fixtures.plaid_item_fixtures import plaid_item_factory, valid_create_request_factory,\
    valid_update_request_factory


def cannot_construct_invalid_create_request(profile_factory):
    with pytest.raises(ValidationError):
        profile = profile_factory()
        return CreatePlaidItemSchema().load({
            'profile_id': profile.id,
            'item_id': id_generator(),
            'request_id': id_generator(),
            'status': ''
        })


def cannot_construct_invalid_update_request(plaid_item_factory):
    with pytest.raises(ValidationError):
        item = plaid_item_factory()
        return UpdatePlaidItemSchema().load({
            'id': item.id,
            'status': 'updated',
            'access_token': id_generator()
        })


def test_get_plaid_item_by_id_returns_plaid_item(db, plaid_item_factory):
    item = plaid_item_factory()
    result = get_plaid_item_by_id(db, item.id)
    assert result.success
    assert result.data.id == item.id


def test_get_plaid_item_by_id_fails_if_item_missing(db):
    result = get_plaid_item_by_id(db, 23423)
    assert not result.success
    assert result.data is None


def test_get_plaid_item_by_plaid_item_id_returns_plaid_item(db, plaid_item_factory):
    item = plaid_item_factory()
    result = get_plaid_item_by_plaid_item_id(db, item.item_id)
    assert result.success
    assert result.data.id == item.id


def test_get_plaid_item_by_plaid_item_id_fails_if_item_missing(db):
    result = get_plaid_item_by_id(db, 'fake-plaid-id')
    assert not result.success
    assert result.data is None


def test_get_plaid_item_by_profile_returns_plaid_item(db, profile_factory, plaid_item_factory):
    profile = profile_factory()
    item = plaid_item_factory(profile_id=profile.id)
    result = get_plaid_items_by_profile(db, profile)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 1
    assert result.data[0].id == item.id
    assert result.data[0].profile_id == profile.id


def test_get_plaid_item_by_profile_fails_if_item_missing(db, profile_factory):
    profile = profile_factory()
    result = get_plaid_items_by_profile(db, profile)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 0


def test_create_plaid_item_accepts_valid_input(db, valid_create_request_factory):
    request = valid_create_request_factory()
    result = create_plaid_item(db, request)
    assert result.success
    assert result.data.id is not None


def test_update_plaid_item_accepts_valid_input(db, plaid_item_factory, valid_update_request_factory):
    item = plaid_item_factory()
    request = valid_update_request_factory()
    request['id'] = item.id
    assert item.status != request['status']
    result = update_plaid_item(db, request)
    assert result.success
    assert result.data is not None
    assert result.data.id == item.id
    assert result.data.status == request['status']


def test_update_plaid_item_fails_if_item_not_found(db, valid_update_request_factory):
    request = valid_update_request_factory()
    request['id'] = 2342342
    result = update_plaid_item(db, request)
    assert not result.success
    assert result.data is None


def test_delete_plaid_item_succeeds_if_exists(db, plaid_item_factory):
    item = plaid_item_factory()
    result = delete_plaid_item(db, item.id)
    assert result.success
    assert get_plaid_item_by_id(db, item.id).data is None


def test_delete_plaid_item_fails_if_missing(db):
    result = delete_plaid_item(db, 132342)
    assert not result.success
    assert result.data is None
