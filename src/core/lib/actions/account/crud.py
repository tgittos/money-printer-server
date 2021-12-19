from datetime import datetime

from sqlalchemy import and_

from core.models.account import Account, AccountSchema
from core.models.profile import Profile
from core.models.plaid_item import PlaidItem
from core.lib.types import AccountList


def create_account(db, request: AccountSchema) -> Account:
    """
    Creates an account object in the given database, and returns it
    """
    r = Account()

    r.profile_id = request.profile_id
    r.plaid_item_id = request.plaid_item_id
    r.account_id = request.account_id
    r.name = request.name
    r.official_name = request.official_name
    r.type = request.type
    r.subtype = request.subtype
    r.timestamp = datetime.utcnow()

    with db.get_session() as session:
        session.add(r)
        session.commit()

    return r


def update_account(db, account: Account) -> Account:
    """
    Updates an account object in the given database, and returns it
    """
    account.timestamp = datetime.utcnow()
    with db.get_session() as session:
        session.attach(account)
        session.commit()

    return account


def create_or_update_account(db, profile: Profile, plaid_link: PlaidItem, account_dict: dict) -> Account:
    """
    Updates the DB record with the remote record data, and creates it if it doesn't exist
    """
    # update the account
    account_id = account_dict['account_id']
    account = get_account_by_account_id(
        db, profile=profile, account_id=account_id)
    if account is None:
        schema = AccountSchema().load({
            'account_id':account_dict['account_id'],
            'name':account_dict['name'],
            'official_name':account_dict['official_name'],
            'type':account_dict['type'],
            'subtype':account_dict['subtype'],
            'plaid_item_id':plaid_link.id,
            'profile_id':profile.id
        })
        account = create_account(db, schema)
    else:
        account.name = account_dict['name']
        account.official_name = account_dict['official_name']
        account.type = account_dict['type'],
        account.subtype = account_dict['subtype']
        update_account(db, account)

    return account


def get_account_by_id(db, profile: Profile, account_id: int) -> Account:
    """
    Gets an account from the database for a given profile by the primary key
    """
    with db.get_session() as session:
        r = session.query(Account).filter(and_(
            Account.profile_id == profile.id,
            Account.id == account_id
        )).first()
    return r


def get_account_by_account_id(db, profile: Profile, account_id: str) -> Account:
    """
    Gets an account from the database from a given profile by the remote account ID
    """
    with db.get_session() as session:
        r = session.query(Account).filter(and_(
            Account.profile_id == profile.id,
            Account.account_id == account_id
        )).first()

    return r


def get_accounts_by_profile(db, profile: Profile) -> AccountList:
    """
    Gets all accounts for a given profile from the database
    """
    with db.get_session() as session:
        r = session.query(Account).filter(
            Account.profile_id == profile.id).all()

    return r


def get_accounts_by_plaid_item(db, plaid_item: PlaidItem) -> AccountList:
    """
    Gets all accounts for a given PlaidItem from the DB
    """
    with db.get_session() as session:
        r = session.query(Account).filter(
            Account.plaid_item_id == plaid_item.id).all()

    return r
