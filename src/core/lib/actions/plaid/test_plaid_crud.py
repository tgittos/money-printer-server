import pytest
from marshmallow import ValidationError

from core.schemas.create_schemas import CreatePlaidItemSchema
from core.schemas.update_schemas import UpdatePlaidItemSchema
from core.lib.actions.plaid.crud import *

from tests.helpers import db
from tests.factories import create_user_profile, create_plaid_item


@pytest.fixture
def existing_profile(db):
    with db.get_session() as session:
        return create_user_profile(session)


@pytest.fixture
def existing_plaid_item(db, existing_profile):
    with db.get_session() as session:
        return create_plaid_item(
            session,
            profile_id=existing_profile.id
        )


@pytest.fixture
def valid_create_request(existing_profile):
    return CreatePlaidItemSchema().load({
        'profile_id': existing_profile.id,
        'item_id': 'thisisanitemid',
        'access_token': 'thisistheaccesstoken',
        'request_id': 'therequestid',
        'status': ''
    })


@pytest.fixture
def valid_update_request(existing_plaid_item):
    return UpdatePlaidItemSchema().load({
        'id': existing_plaid_item.id,
        'status': 'updated'
    })


def cannot_construct_invalid_create_request():
    with pytest.raises(ValidationError):
        return CreatePlaidItemSchema().load({
            'profile_id': existing_profile.id,
            'item_id': 'thisisanitemid',
            'request_id': 'therequestid',
            'status': ''
        })


def cannot_construct_invalid_update_request():
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


def test_get_plaid_item_by_plaid_item_id_returns_plaid_item():
    assert False


def test_get_plaid_item_by_plaid_item_id_fails_if_item_missing():
    assert False


def test_get_plaid_item_by_plaid_item_id_fails_for_id_in_other_profile():
    assert False


def test_get_plaid_item_by_profile_returns_plaid_item():
    assert False


def test_get_plaid_item_by_profile_fails_if_item_missing():
    assert False


def test_get_plaid_item_by_profile_fails_for_id_in_other_profile():
    assert False


def test_create_plaid_item_accepts_valid_intput():
    assert False


def test_create_plaid_item_rejects_invalid_input():
    assert False


def test_update_plaid_item_accepts_valid_input():
    assert False


def test_update_plaid_item_rejects_invalid_input():
    assert False


def test_update_plaid_item_fails_if_item_not_found():
    assert False


def test_delete_plaid_item_succeeds_if_exists():
    assert False


def test_delete_plaid_item_fails_if_missing():
    assert False
