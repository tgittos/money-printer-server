from datetime import datetime
from marshmallow import EXCLUDE

from sqlalchemy import and_, desc

from core.models import Account, AccountBalance
from core.schemas import CreateAccountSchema, UpdateAccountSchema, CreateAccountBalanceSchema, UpdateAccountBalanceSchema
from core.actions.action_response import ActionResponse


def create_account(db, profile_id: int, plaid_item_id: int, request: CreateAccountSchema) -> ActionResponse:
    """
    Creates an account object in the given database, and returns it
    """
    account = Account()

    account.profile_id = profile_id
    account.plaid_item_id = plaid_item_id
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


def update_account(db, profile_id: int, request: UpdateAccountSchema) -> ActionResponse:
    """
    Updates an account object in the given database, and returns it
    """
    result = get_account_by_id(db, profile_id, request['id'])

    if not result.success or result.data is None:
        return ActionResponse(
            success=False,
            message=f"Account with ID {request['id']} not found"
        )

    account = result.data

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


def create_or_update_account(db, profile_id: int, plaid_item_id: int, account_dict: dict) -> ActionResponse:
    """
    Updates the DB record with the remote record data, and creates it if it doesn't exist
    """
    # update the account
    account_id = account_dict['account_id']
    get_result = get_account_by_account_id(
        db, profile_id=profile_id, account_id=account_id)
    account = get_result.data
    if account is None:
        schema = CreateAccountSchema().load(account_dict)
        return create_account(db, profile_id, plaid_item_id, schema)
    else:
        schema = UpdateAccountSchema().load(account_dict)
        return update_account(db, profile_id, schema)


def get_account_by_id(db, profile_id: int, account_id: int) -> ActionResponse:
    """
    Gets an account from the database for a given profile by the primary key
    """
    with db.get_session() as session:
        account = session.query(Account).filter(and_(
            Account.profile_id == profile_id,
            Account.id == account_id
        )).first()

    return ActionResponse(
        success=account is not None,
        data=account,
        message=f"Account with ID {account_id} not found" if account is None else None
    )


def get_account_by_account_id(db, profile_id: int, account_id: str) -> ActionResponse:
    """
    Gets an account from the database from a given profile by the remote account ID
    """
    with db.get_session() as session:
        account = session.query(Account).filter(and_(
            Account.profile_id == profile_id,
            Account.account_id == account_id
        )).first()

    return ActionResponse(
        success=account is not None,
        data=account,
        message=f"Account with account_id {account_id} not found" if account is None else None
    )


def get_accounts_by_profile_id(db, profile_id: int) -> ActionResponse:
    """
    Gets all accounts for a given profile from the database
    """
    with db.get_session() as session:
        accounts = session.query(Account).filter(
            Account.profile_id == profile_id).all()

    return ActionResponse(
        success=accounts is not None,
        data=accounts,
        message=f"No accounts with profile ID {profile_id} found" if accounts is None else None
    )


def get_accounts_by_plaid_item_id(db, profile_id: int, plaid_item_id: int) -> ActionResponse:
    """
    Gets all accounts for a given PlaidItem from the DB
    """
    with db.get_session() as session:
        accounts = session.query(Account).filter(
            Account.plaid_item_id == plaid_item_id).all()

    return ActionResponse(
        success=accounts is not None,
        data=accounts,
        message=f"No accounts with plaid_item ID {plaid_item_id} found" if accounts is None else None
    )


def create_account_balance(db, profile_id: int, request: CreateAccountBalanceSchema) -> ActionResponse:
    """
    Creates an AccountBalance record in the DB, to snapshot the account value at a point in time
    """
    balance = AccountBalance()

    balance.account_id = request['account_id']
    balance.available = request['available']
    balance.current = request['current']
    balance.iso_currency_code = request['iso_currency_code']
    balance.timestamp = datetime.utcnow()

    with db.get_session() as session:
        session.add(balance)
        session.commit()

    return ActionResponse(
        success=balance is not None,
        data=balance
    )


def get_balances_by_account(db, profile_id: int, account_id: int, start=None, end=None) -> ActionResponse:
    """
    Returns all the balances for the requested account
    Accepts an object of GetAccountBalanceRequest type
    """
    records = []
    if account_id is not None:
        with db.get_session() as session:
            if start is not None:
                if end is not None:
                    records = session.query(AccountBalance).filter(and_(
                        AccountBalance.account_id == account_id,
                        start <= AccountBalance.timestamp,
                        AccountBalance.timestamp <= end
                    )).all()
                else:
                    records = session.query(AccountBalance).filter(and_(
                        AccountBalance.account_id == account_id,
                        start <= AccountBalance.timestamp)
                    ).all()
            else:
                if end is not None:
                    records = session.query(AccountBalance).filter(and_(
                        AccountBalance.account_id == account_id,
                        AccountBalance.timestamp <= end
                    )).all()
                else:
                    records = session.query(AccountBalance).filter(
                        AccountBalance.account_id == account_id).all()

        return ActionResponse(
            success=True,
            data=records
        )
    return ActionResponse(
        success=False,
        message="Account ID passed None value"
    )


def get_latest_balance_by_account(db, profile_id: int, account_id: int) -> ActionResponse:
    """
    Returns the last synced balance for the given account
    """
    with db.get_session() as session:
        balance = session.query(AccountBalance).filter(
            AccountBalance.account_id == account_id).order_by(
                desc(AccountBalance.timestamp)).first()

    return ActionResponse(
        success=balance is not None,
        data=balance,
        message=f"No balances found for account ID {account_id}" if balance is None else None
    )
