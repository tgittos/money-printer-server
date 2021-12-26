import pytest
from marshmallow import ValidationError

from core.schemas.plaid_item_schemas import CreatePlaidItemSchema, UpdatePlaidItemSchema
from core.actions.plaid.crud import *

from tests.fixtures.core import db
from tests.fixtures.profile_fixtures import existing_profile, profile_with_no_plaids
from tests.fixtures.plaid_item_fixtures import existing_plaid_item, valid_create_request,\
    valid_update_request


def cannot_construct_invalid_create_request(existing_profile):
    with pytest.raises(ValidationError):
        return CreatePlaidItemSchema().load({
            'profile_id': existing_profile.id,
            'item_id': 'thisisanitemid',
            'request_id': 'therequestid',
            'status': ''
        })


def cannot_construct_invalid_update_request(existing_plaid_item):
    with pytest.raises(ValidationError):
        return UpdatePlaidItemSchema().load({
            'id': existing_plaid_item.id,
            'status': 'updated',
            'access_token': 'thisistheupdatedtoken'
        })


def test_get_plaid_item_by_id_returns_plaid_item(db, existing_plaid_item):
    result = get_plaid_item_by_id(db, existing_plaid_item.id)
    assert result.success
    assert result.data.id == existing_plaid_item.id


def test_get_plaid_item_by_id_fails_if_item_missing(db):
    result = get_plaid_item_by_id(db, 23423)
    assert not result.success
    assert result.data is None


def test_get_plaid_item_by_plaid_item_id_returns_plaid_item(db, existing_plaid_item):
    result = get_plaid_item_by_plaid_item_id(db, existing_plaid_item.item_id)
    assert result.success
    assert result.data.id == existing_plaid_item.id


def test_get_plaid_item_by_plaid_item_id_fails_if_item_missing(db):
    result = get_plaid_item_by_id(db, 'fake-plaid-id')
    assert not result.success
    assert result.data is None


def test_get_plaid_item_by_profile_returns_plaid_item(db, existing_plaid_item, existing_profile):
    result = get_plaid_items_by_profile(db, existing_profile)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 1
    assert result.data[0].id == existing_plaid_item.id
    assert result.data[0].profile_id == existing_profile.id


def test_get_plaid_item_by_profile_fails_if_item_missing(db, profile_with_no_plaids):
    result = get_plaid_items_by_profile(db, profile_with_no_plaids)
    assert result.success
    assert result.data is not None
    assert len(result.data) == 0


def test_create_plaid_item_accepts_valid_intput(db, valid_create_request):
    result = create_plaid_item(db, valid_create_request)
    assert result.success
    assert result.data.id is not None


def test_update_plaid_item_accepts_valid_input():
    assert False


def test_update_plaid_item_fails_if_item_not_found(db, valid_update_request):
    valid_update_request['id'] = 2342342
    result = update_plaid_item(db, valid_update_request)
    assert not result.success
    assert result.data is None


def test_delete_plaid_item_succeeds_if_exists(db, existing_plaid_item):
    result = delete_plaid_item(db, existing_plaid_item.id)
    assert result.success
    assert get_plaid_item_by_id(db, existing_plaid_item.id).data is None


def test_delete_plaid_item_fails_if_missing(db):
    result = delete_plaid_item(db, 132342)
    assert not result.success
    assert result.data is None
