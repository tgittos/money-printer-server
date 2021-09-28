from datetime import datetime

from sqlalchemy import and_, desc

from core.models.account_balance import AccountBalance
from core.models.account import Account
from core.lib.types import AccountBalanceList

from .requests import GetAccountBalanceRequest, CreateAccountBalanceRequest


def create_account_balance(cls, request: CreateAccountBalanceRequest) -> AccountBalance:
    """
    Creates an AccountBalance record in the DB, to snapshot the account value at a point in time
    """
    balance = AccountBalance()
    balance.account_id = request.account.id
    balance.available = request.available
    balance.current = request.current
    balance.iso_currency_code = request.iso_currency_code
    balance.timestamp = datetime.utcnow()

    def create(session):
        session.add(balance)
        session.commit()

    cls.db.with_session(create)

    return balance


def get_balances_by_account(cls, request: GetAccountBalanceRequest) -> AccountBalanceList:
    """
    Returns all the balances for the requested account
    Accepts an object of GetAccountBalanceRequest type
    """
    records = []
    if request.account is not None:
        if request.start is not None:
            if request.end is not None:
                records = cls.db.with_session(lambda session: session.query
                                              .filter(and_(
                                                  AccountBalance.account_id == request.account.id,
                                                  request.start <= AccountBalance.timestamp <= request.end
                                              )).all()
                                              )
            else:
                records = cls.db.with_session(lambda session: session.query
                                              .filter(and_(
                                                  AccountBalance.account_id == request.account.id,
                                                  request.start <= AccountBalance.timestamp)
                                              ).all()
                                              )
        else:
            records = cls.db.with_session(lambda session: session.query(AccountBalance)
                                          .filter(AccountBalance.account_id == request.account.id).all()
                                          )
    return records


def get_latest_balance_by_account(self, account: Account) -> AccountBalance:
    """
    Returns the last synced balance for the given account
    """
    r = self.db.with_session(lambda session: session.query(AccountBalance)
                             .filter(AccountBalance.accountId == account.id).order_by(
                                desc(AccountBalance.timestamp)).first()
                             )
    return r
