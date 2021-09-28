from datetime import datetime

from sqlalchemy import and_

from core.models.account import Account
from core.models.profile import Profile
from core.models.plaid_item import PlaidItem
from core.lib.types import AccountList

from .requests import CreateAccountRequest


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

    def create(session):
        session.add(r)
        session.commit()

    cls.db.with_session(create)

    return r


def update_account(cls, account: Account) -> Account:
    """
    Updates an account object in the given database, and returns it
    """
    account.timestamp = datetime.utcnow()
    cls.db.with_session(lambda session: session.commit())
    return account


def create_or_update_account(cls, profile: Profile, plaid_link: PlaidItem, account_dict: dict) -> Account:
    """
    Updates the DB record with the remote record data, and creates it if it doesn't exist
    """
    # update the account
    account_id = account_dict['account_id']
    account = get_account_by_account_id(cls, profile=profile, account_id=account_id)
    if account is None:
        if cls.logger:
            cls.logger.debug("creating new account from account_dict: {0}".format(account_dict))
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
        if cls.logger:
            cls.logger.debug("found existing account {0}, updating: {1}".format(account.id, account_dict))
        account.name = account_dict['name']
        account.official_name = account_dict['official_name']
        account.type = account_dict['type'],
        account.subtype = account_dict['subtype']
        update_account(cls, account)

    return account


def get_account_by_id(cls, profile: Profile, account_id: int) -> Account:
    """
    Gets an account from the database for a given profile by the primary key
    """
    r = cls.db.with_session(lambda session: session.query(Account)
                            .filter(and_(
                                Account.profile_id == profile.id,
                                Account.id == account_id
                            )).first()
                            )
    return r


def get_account_by_account_id(cls, profile: Profile, account_id: str) -> Account:
    """
    Gets an account from the database from a given profile by the remote account ID
    """
    r = cls.db.with_session(lambda session: session.query(Account)
                            .filter(and_(
                                Account.profile_id == profile.id,
                                Account.account_id == account_id
                            )).first()
                            )
    return r


def get_accounts_by_profile(cls, profile: Profile) -> AccountList:
    """
    Gets all accounts for a given profile from the database
    """
    r = cls.db.with_session(lambda session: session.query(Account)
                            .filter(Account.profile_id == profile.id).all()
                            )
    return r


def get_accounts_by_plaid_item(cls, plaid_item: PlaidItem) -> AccountList:
    """
    Gets all accounts for a given PlaidItem from the DB
    """
    r = cls.db.with_session(lambda session: session.query(Account)
                            .filter(Account.plaid_item_id == plaid_item.id).all()
                            )
    return r
