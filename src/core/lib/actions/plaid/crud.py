from datetime import datetime

from core.models.profile import Profile
from core.models.plaid_item import PlaidItem
from core.lib.types import PlaidItemList

from .requests import CreatePlaidItem


def get_plaid_item_by_id(db, id: int) -> PlaidItem:
    """
    Gets a PlaidItem from the DB by the primary key
    This object represents a Plaid Link object
    """
    r = db.with_session(lambda session: session.query(PlaidItem).filter(PlaidItem.id == id).first())
    return r


def get_plaid_item_by_plaid_item_id(db, id: str) -> PlaidItem:
    """
    Gets a PlaidItem from the DB by the remote Plaid ID
    This object represents a Plaid Link object
    """
    r = db.with_session(lambda session: session.query(PlaidItem).filter(PlaidItem.item_id == id).first())
    return r


def get_plaid_items_by_profile(db, profile: Profile) -> PlaidItemList:
    """
    Returns all the PlaidItems associated with the given profile
    """
    r = db.with_session(lambda session: session.query(PlaidItem).where(PlaidItem.profile_id == profile.id).all())
    return r


def create_plaid_item(db, request: CreatePlaidItem) -> PlaidItem:
    """
    Creates a PlaidItem in the DB with the data in the given request
    Accepts a CreatePlaidItem object
    """
    r = PlaidItem()
    r.profile_id = request.profile_id
    r.item_id = request.item_id
    r.access_token = request.access_token
    r.request_id = request.request_id
    r.timestamp = datetime.utcnow()

    def create(session):
        session.add(r)
        session.commit()

    db.with_session(create)

    return r


def update_plaid_item(db, plaid_item: PlaidItem) -> PlaidItem:
    """
    Updates a PlaidItem in the DB and touches the timestamp for it
    """
    plaid_item.timestamp = datetime.utcnow()
    db.with_session(lambda session: session.commit())
    return plaid_item
