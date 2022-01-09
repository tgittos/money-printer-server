from sqlalchemy import and_
from sqlalchemy.exc import DBAPIError
from datetime import datetime
import json

from core.models import Profile, PlaidItem
from core.schemas import CreatePlaidItemSchema, UpdatePlaidItemSchema
from core.actions.action_response import ActionResponse


def get_plaid_item_by_id(db, profile_id: int, id: int) -> ActionResponse:
    """
    Gets a PlaidItem from the DB by the primary key
    This object represents a Plaid Link object
    """
    try:
        with db.get_session() as session:
            plaid_item = session.query(PlaidItem).filter(
                and_(
                    PlaidItem.profile_id == profile_id,
                    PlaidItem.id == id
                )).first()

        return ActionResponse(
            success=plaid_item is not None,
            data=plaid_item,
            message=f"No plaid item found with ID {id}" if plaid_item is None else None
        )
    except DBAPIError as err:
        print(f"Error while running SQL:", err.statement, json.dumps(err.params))
        return ActionResponse(success=False,data=err)


def get_plaid_item_by_plaid_item_id(db, profile_id: int, id: str) -> ActionResponse:
    """
    Gets a PlaidItem from the DB by the remote Plaid ID
    This object represents a Plaid Link object
    """
    with db.get_session() as session:
        plaid_item = session.query(PlaidItem).filter(
            and_(
                PlaidItem.profile_id == profile_id,
                PlaidItem.item_id == id
            )).first()

    return ActionResponse(
        success=plaid_item is not None,
        data=plaid_item,
        message=f"No plaid item found with plaid item ID {id}" if plaid_item is None else None
    )


def get_plaid_items_by_profile_id(db, profile_id: int) -> ActionResponse:
    """
    Returns all the PlaidItems associated with the given profile
    """
    with db.get_session() as session:
        plaid_items = session.query(PlaidItem).where(
            PlaidItem.profile_id == profile_id).all()

    return ActionResponse(
        success=plaid_items is not None,
        data=plaid_items,
        message=f"No plaid item found with profile ID {id}" if plaid_items is None else None
    )


def create_plaid_item(db, profile_id: int, request: CreatePlaidItemSchema) -> ActionResponse:
    """
    Creates a PlaidItem in the DB with the data in the given request
    Accepts a PlaidItemSchema object
    """
    plaid_item = PlaidItem()

    plaid_item.profile_id = profile_id
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


def update_plaid_item(db, profile_id: int, request: UpdatePlaidItemSchema) -> ActionResponse:
    """
    Updates a PlaidItem in the DB and touches the timestamp for it
    """
    result = get_plaid_item_by_id(db, profile_id, request['id'])
    if not result.success or result.data is None:
        return ActionResponse(
            success=False,
            message=f"No plaid item found with ID {request['id']}"
        )

    plaid_item = result.data

    with db.get_session() as session:
        session.add(plaid_item)

        plaid_item.status = request['status']
        plaid_item.timestamp = datetime.utcnow()

        session.commit()

    return ActionResponse(
        success=True,
        data=plaid_item
    )


def delete_plaid_item(db, profile_id: int, plaid_item_id: int) -> ActionResponse:
    result = get_plaid_item_by_id(db, profile_id, plaid_item_id)
    if not result.success or result.data is None:
        return ActionResponse(
            success=False,
            message=f"Could not find plaid_item with ID {plaid_item_id}"
        )

    with db.get_session() as session:
        session.delete(result.data)
        session.commit()

    return ActionResponse(
        success=True
    )
