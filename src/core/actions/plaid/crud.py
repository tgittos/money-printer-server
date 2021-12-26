from datetime import datetime

from core.models.profile import Profile
from core.models.plaid_item import PlaidItem
from core.schemas.plaid_item_schemas import CreatePlaidItemSchema, UpdatePlaidItemSchema
from core.actions.action_response import ActionResponse


def get_plaid_item_by_id(db, id: int) -> ActionResponse:
    """
    Gets a PlaidItem from the DB by the primary key
    This object represents a Plaid Link object
    """
    with db.get_session() as session:
        plaid_item = session.query(PlaidItem).filter(
            PlaidItem.id == id).first()

    return ActionResponse(
        success=plaid_item is not None,
        data=plaid_item,
        message=f"No plaid item found with ID {id}" if plaid_item is None else None
    )


def get_plaid_item_by_plaid_item_id(db, id: str) -> ActionResponse:
    """
    Gets a PlaidItem from the DB by the remote Plaid ID
    This object represents a Plaid Link object
    """
    with db.get_session() as session:
        plaid_item = session.query(PlaidItem).filter(
            PlaidItem.item_id == id).first()

    return ActionResponse(
        success=plaid_item is not None,
        data=plaid_item,
        message=f"No plaid item found with plaid item ID {id}" if plaid_item is None else None
    )


def get_plaid_items_by_profile(db, profile: Profile) -> ActionResponse:
    """
    Returns all the PlaidItems associated with the given profile
    """
    with db.get_session() as session:
        plaid_items = session.query(PlaidItem).where(
            PlaidItem.profile_id == profile.id).all()

    return ActionResponse(
        success=plaid_items is not None,
        data=plaid_items,
        message=f"No plaid item found with profile ID {id}" if plaid_items is None else None
    )


def create_plaid_item(db, request: CreatePlaidItemSchema) -> ActionResponse:
    """
    Creates a PlaidItem in the DB with the data in the given request
    Accepts a PlaidItemSchema object
    """
    plaid_item = PlaidItem()

    plaid_item.profile_id = request['profile_id']
    plaid_item.item_id = request['item_id']
    plaid_item.access_token = request['access_token']
    plaid_item.request_id = request['request_id']
    plaid_item.timestamp = datetime.utcnow()

    with db.get_session() as session:
        session.add(plaid_item)
        session.commit()

    return ActionResponse(
        success=True,
        data=plaid_item
    )


def update_plaid_item(db, request: UpdatePlaidItemSchema) -> ActionResponse:
    """
    Updates a PlaidItem in the DB and touches the timestamp for it
    """
    plaid_item = get_plaid_item_by_id(request['id'])
    if plaid_item is None:
        return ActionResponse(
            success=False,
            message=f"No plaid item found with ID {request['id']}"
        )

    with db.get_session() as session:
        session.add(plaid_item)

        plaid_item.item_id = request['item_id']
        plaid_item.access_token = request['access_token']
        plaid_item.request_id = request['request_id']
        plaid_item.timestamp = datetime.utcnow()

        session.commit()

    return ActionResponse(
        success=True,
        data=plaid_item
    )


def delete_plaid_item(db, plaid_item_id: int):
    raise Exception("not implemented yet")
