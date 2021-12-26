from datetime import datetime
from marshmallow import EXCLUDE

from sqlalchemy import and_

from core.models.account import Account
from core.models.profile import Profile
from core.models.plaid_item import PlaidItem
from core.schemas.account_schemas import CreateAccountSchema, ReadAccountSchema, UpdateAccountSchema
from core.actions.action_response import ActionResponse


def create_account(db, request: CreateAccountSchema) -> ActionResponse:
    """
    Creates an account object in the given database, and returns it
    """
    account = Account()

    account.profile_id = request['profile_id']
    account.plaid_item_id = request['plaid_item_id']
    account.account_id = request['account_id']
    account.name = request['name']
    account.official_name = request['official_name']
    account.type = request['type']
    account.subtype = request['subtype']
    account.timestamp = datetime.utcnow()

    with db.get_session() as session:
        session.add(account)
        session.commit()

    return ActionResponse(
        success=account.id is not None,
        data=account
    )


def update_account(db, request: UpdateAccountSchema) -> ActionResponse:
    """
    Updates an account object in the given database, and returns it
    """
    account = get_account_by_id(request['id'])

    if account is None:
        return ActionResponse(
            success=False,
            message=f"Account with ID {request['id']} not found"
        )

    with db.get_session() as session:
        session.add(account)

        account.account_id = request['account_id']
        account.name = request['name']
        account.official_name = request['official_name']
        account.type = request['type']
        account.subtype = request['subtype']
        account.timestamp = datetime.utcnow()

        session.commit()

    return ActionResponse(
        success=True,
        data=account
    )


def create_or_update_account(db, profile: Profile, plaid_link: PlaidItem, account_dict: dict) -> ActionResponse:
    """
    Updates the DB record with the remote record data, and creates it if it doesn't exist
    """
    # update the account
    account_id = account_dict['account_id']
    account = get_account_by_account_id(
        db, profile=profile, account_id=account_id)
    if account is None:
        schema = CreateAccountSchema().load(
            {**{'plaid_item_id': plaid_link.id, 'profile_id': profile.id}, **account_dict}
        )
        account = create_account(db, schema)
    else:
        schema = UpdateAccountSchema(unknown=EXCLUDE).load(
            {**{'id': account_id}, **account_dict})
        update_account(db, schema)

    return ActionResponse(
        success=account is not None,
        data=account
    )


def get_account_by_id(db, profile: Profile, account_id: int) -> ActionResponse:
    """
    Gets an account from the database for a given profile by the primary key
    """
    with db.get_session() as session:
        account = session.query(Account).filter(and_(
            Account.profile_id == profile.id,
            Account.id == account_id
        )).first()

    return ActionResponse(
        success=account is not None,
        data=account,
        message=f"Account with ID {account_id} not found" if account is None else None
    )


def get_account_by_account_id(db, profile: Profile, account_id: str) -> ActionResponse:
    """
    Gets an account from the database from a given profile by the remote account ID
    """
    with db.get_session() as session:
        account = session.query(Account).filter(and_(
            Account.profile_id == profile.id,
            Account.account_id == account_id
        )).first()

    return ActionResponse(
        success=account is not None,
        data=account,
        message=f"Account with account_id {account_id} not found" if account is None else None
    )


def get_accounts_by_profile(db, profile: Profile) -> ActionResponse:
    """
    Gets all accounts for a given profile from the database
    """
    with db.get_session() as session:
        accounts = session.query(Account).filter(
            Account.profile_id == profile.id).all()

    return ActionResponse(
        success=accounts is not None,
        data=accounts,
        message=f"No accounts with profile ID {profile.id} found" if accounts is None else None
    )


def get_accounts_by_plaid_item(db, plaid_item: PlaidItem) -> ActionResponse:
    """
    Gets all accounts for a given PlaidItem from the DB
    """
    with db.get_session() as session:
        accounts = session.query(Account).filter(
            Account.plaid_item_id == plaid_item.id).all()

    return ActionResponse(
        success=accounts is not None,
        data=accounts,
        message=f"No accounts with plaid_item ID {plaid_item.id} found" if accounts is None else None
    )
