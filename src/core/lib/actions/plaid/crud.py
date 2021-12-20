from datetime import datetime

from core.models.profile import Profile
from core.models.plaid_item import PlaidItem, PlaidItemSchema
from core.lib.types import PlaidItemList


def get_plaid_item_by_id(db, id: int) -> PlaidItem:
    """
    Gets a PlaidItem from the DB by the primary key
    This object represents a Plaid Link object
    """
    with db.get_session() as session:
        r = session.query(PlaidItem).filter(PlaidItem.id == id).first()
    return r


def get_plaid_item_by_plaid_item_id(db, id: str) -> PlaidItem:
    """
    Gets a PlaidItem from the DB by the remote Plaid ID
    This object represents a Plaid Link object
    """
    with db.get_session() as session:
        r = session.query(PlaidItem).filter(PlaidItem.item_id == id).first()
    return r


def get_plaid_items_by_profile(db, profile: Profile) -> PlaidItemList:
    """
    Returns all the PlaidItems associated with the given profile
    """
    with db.get_session() as session:
        r = session.query(PlaidItem).where(
            PlaidItem.profile_id == profile.id).all()
    return r


def create_plaid_item(db, request: PlaidItemSchema) -> PlaidItem:
    """
    Creates a PlaidItem in the DB with the data in the given request
    Accepts a PlaidItemSchema object
    """
    r = PlaidItem()
    r.profile_id = request.profile_id
    r.item_id = request.item_id
    r.access_token = request.access_token
    r.request_id = request.request_id
    r.timestamp = datetime.utcnow()

    with db.get_session() as session:
        session.add(r)
        session.commit()

    return r


def update_plaid_item(db, plaid_item: PlaidItem) -> PlaidItem:
    """
    Updates a PlaidItem in the DB and touches the timestamp for it
    """
    plaid_item.timestamp = datetime.utcnow()
    with db.get_session() as session:
        session.attach(plaid_item)
        session.commit()
    return plaid_item
