from datetime import datetime

from sqlalchemy import and_

from core.models.account import Account
from core.models.profile import Profile
from core.models.plaid_item import PlaidItem
from core.lib.types import AccountList

from .requests import CreateAccountRequest


@classmethod
def create_account(cls, request: CreateAccountRequest) -> Account:
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

    cls.db.add(r)
    cls.db.commit()

    return r


@classmethod
def update_account(cls, account: Account) -> Account:
    """
    Updates an account object in the given database, and returns it
    """
    account.timestamp = datetime.utcnow()
    cls.db.commit()
    return account

@classmethod
def create_or_update_account(cls, profile: Profile, plaid_link: PlaidItem, account_dict: dict) -> Account:
    """
    Updates the DB record with the remote record data, and creates it if it doesn't exist
    """
    # update the account
    account = cls.get_account_by_account_id(profile=profile, account_id=account_dict['account_id'])
    if account is None:
        account = create_account(cls, CreateAccountRequest(
            account_id=account_dict['account_id'],
            name=account_dict['name'],
            official_name=account_dict['official_name'],
            type=account_dict['type'],
            subtype=account_dict['subtype'],
            plaid_item_id=plaid_link.id,
            profile_id=profile.id
        ))
    else:
        account.name = account_dict['name']
        account.official_name = account_dict['official_name']
        account.type = account_dict['type'],
        account.subtype = account_dict['subtype']
        update_account(cls, account)

    return account


@classmethod
def get_account_by_id(cls, profile: Profile, account_id: int) -> Account:
    """
    Gets an account from the database for a given profile by the primary key
    """
    r = cls.db.query(Account).where(and_(
        Account.profile_id == profile.id,
        Account.id == account_id
    )).first()
    return r


@classmethod
def get_account_by_account_id(cls, profile: Profile, account_id: str) -> Account:
    """
    Gets an account from the database from a given profile by the remote account ID
    """
    r = cls.db.query(Account).where(and_(
        Account.profile_id == profile.id,
        Account.account_id == account_id)).first()
    return r


@classmethod
def get_accounts_by_profile(cls, profile: Profile) -> AccountList:
    """
    Gets all accounts for a given profile from the database
    """
    r = cls.db.query(Account).filter(Account.profile_id == profile.id).all()
    return r


@classmethod
def get_accounts_by_plaid_item(cls, plaid_item: PlaidItem) -> AccountList:
    """
    Gets all accounts for a given PlaidItem from the DB
    """
    r = cls.db.query(Account).filter(Account.plaid_item_id == plaid_item.id).all()
    return r
