from datetime import datetime

from sqlalchemy import and_, desc

from core.models.account_balance import AccountBalance, AccountBalanceSchema
from core.models.account import Account
from core.lib.types import AccountBalanceList

from .requests import GetAccountBalanceRequest


def create_account_balance(db, request: AccountBalanceSchema) -> AccountBalance:
    """
    Creates an AccountBalance record in the DB, to snapshot the account value at a point in time
    """
    balance = AccountBalance()
    balance.account_id = request.account.id
    balance.available = request.available
    balance.current = request.current
    balance.iso_currency_code = request.iso_currency_code
    balance.timestamp = datetime.utcnow()

    with db.get_session() as session:
        session.add(balance)
        session.commit()

    return balance


def get_balances_by_account(db, request: GetAccountBalanceRequest) -> AccountBalanceList:
    """
    Returns all the balances for the requested account
    Accepts an object of GetAccountBalanceRequest type
    """
    records = []
    if request.account is not None:
        with db.get_session() as session:
            if request.start is not None:
                if request.end is not None:
                    records = session.query.filter(and_(
                        AccountBalance.account_id == request.account.id,
                        request.start <= AccountBalance.timestamp <= request.end
                    )).all()
                else:
                    records = session.query.filter(and_(
                        AccountBalance.account_id == request.account.id,
                        request.start <= AccountBalance.timestamp)
                    ).all()
            else:
                records = session.query(AccountBalance).filter(
                    AccountBalance.account_id == request.account.id).all()

    return records


def get_latest_balance_by_account(db, account: Account) -> AccountBalance:
    """
    Returns the last synced balance for the given account
    """
    with db.get_session() as session:
        r = session.query(AccountBalance).filter(
            AccountBalance.accountId == account.id).order_by(
                desc(AccountBalance.timestamp)).first()

    return r
