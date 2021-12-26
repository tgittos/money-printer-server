from core.repositories.plaid_repository import PlaidRepository
from tests.factories import create_plaid_item
from tests.fixtures.core import db


def test_get_plaid_item_by_id_returns_plaid_item(db):
    repo = PlaidRepository()
    with db.get_session() as session:
        item = create_plaid_item(session)
    result = repo.get_plaid_item_by_id(item.id)
    assert result.success
    assert result.data is not None
    assert item.id == result.data.id


def test_get_plaid_item_by_id_returns_none_with_missing_id(db):
    repo = PlaidRepository()
    result = repo.get_plaid_item_by_id(23421)
    assert not result.success
    assert result.data is None
