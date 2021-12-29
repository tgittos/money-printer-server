from datetime import datetime

from sqlalchemy import and_, desc

from core.models.account import Account
from core.models.account_balance import AccountBalance
from core.schemas.account_schemas import CreateAccountBalanceSchema, UpdateAccountBalanceSchema
from core.actions.action_response import ActionResponse


def create_account_balance(db, request: CreateAccountBalanceSchema) -> ActionResponse:
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


def get_balances_by_account(db, account_id: int, start=None, end=None) -> ActionResponse:
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


def get_latest_balance_by_account(db, account_id: int) -> ActionResponse:
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
