from core.repositories.plaid_repository import PlaidRepository
from tests.factories import create_plaid_item
from tests.helpers import db


def test_get_plaid_item_by_id_returns_plaid_item(db):
    repo = PlaidRepository(db)
    s = db.get_session()
    item = create_plaid_item(s)
    item_id = item.id
    s.close()
    result = repo.get_plaid_item_by_id(item_id)
    assert item_id == result.id


def test_get_plaid_item_by_id_returns_none_with_missing_id(db):
    repo = PlaidRepository(db)
    result = repo.get_plaid_item_by_id(23421)
    assert result is None
