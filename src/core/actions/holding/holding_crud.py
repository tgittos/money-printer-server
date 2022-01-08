from sqlalchemy import and_
from sqlalchemy.orm import selectinload, lazyload
from datetime import datetime, timezone

from sqlalchemy.util.langhelpers import symbol

from core.models import Holding, HoldingBalance, Account, InvestmentTransaction
from core.schemas import CreateHoldingSchema, UpdateHoldingSchema, CreateHoldingBalanceSchema,\
    UpdateHoldingBalanceSchema, CreateInvestmentTransactionSchema
from core.actions.action_response import ActionResponse
from core.actions.account.crud import get_account_by_id
from core.lib.utilities import sanitize_float


def get_holding_by_id(db, profile_id: int, holding_id: int) -> ActionResponse:
    """
    Gets a holding record from the DB by the primary key
    """
    with db.get_session() as session:
        holding = session.query(Holding)\
            .options(selectinload(Holding.account))\
            .options(selectinload(Holding.balances))\
            .options(selectinload(Holding.security))\
            .filter(and_(
                Holding.id == holding_id,
                Holding.account_id == Account.id,
                Account.profile_id == profile_id
            )).first()
    return ActionResponse(
        success=holding is not None,
        data=holding,
        message=f"Could not find holding with ID {holding_id}" if holding is None else None
    )


def get_holdings_by_account_id(db, profile_id: int, account_id: int) -> ActionResponse:
    """
    Gets all holdings that belong to an account record by it's ID
    """
    with db.get_session() as session:
        holding = session.query(Holding)\
            .options(selectinload(Holding.account))\
            .options(selectinload(Holding.balances))\
            .options(selectinload(Holding.security))\
            .filter(and_(
                Holding.account_id == account_id,
                Holding.account_id == Account.id,
                Account.profile_id == profile_id
            ))\
            .all()
    return ActionResponse(
        success=holding is not None,
        data=holding,
        message=f"Could not find holdings with account_id ID {account_id}" if holding is None else None
    )


def get_holdings_by_profile_id(db, profile_id: int) -> ActionResponse:
    """
    Returns the holdings for a given profile ID
    """
    with db.get_session() as session:
        data = session.query(Holding)\
            .options(selectinload(Holding.account))\
            .options(selectinload(Holding.balances))\
            .options(selectinload(Holding.security))\
            .filter(and_(
                Account.profile_id == profile_id,
                Holding.account_id == Account.id
            )).all()
    return ActionResponse(
        success=data is not None,
        data=data
    )


def get_holdings_by_profile_id_and_account_id(db, profile_id: int, account_id: int) -> ActionResponse:
    # TODO - I need to re-write this SQL to pull in the holdings and the attached securities
    # and return that for schema dumping
    with db.get_session() as session:
        account = session.query(Account).where(and_(
            Account.profile_id == profile_id,
            Account.id == account_id,
        )).first()
        if account is None:
            return ActionResponse(
                success=False,
                message=f"Could not find account with ID {account_id}"
            )
        holdings = session.query(Holding).where(
            Holding.account_id == account.id).all()
    return ActionResponse(
        success=holdings is not None,
        data=holdings,
        message=f"No holdings found for account {account.id}" if holdings is None else None
    )


def get_holding_by_plaid_account_id_and_plaid_security_id(db, plaid_account_id: str,
                                                          plaid_security_id: str) -> ActionResponse:
    """
    Gets a Holding for a Plaid account ID and Plaid security ID
    """
    # TODO - this method doesn't make much sense - there might be multiple holdings at different avg costs?
    with db.get_session() as session:
        account = session.query(Account).where(
            Account.account_id == plaid_account_id).first()
        record = session.query(Holding).where(
            Holding.account_id == account.id
        ).first()

    return ActionResponse(
        success=record is not None,
        data=record,
        message=f"No holding found for plaid_account_id {plaid_account_id} and plaid_security_id {plaid_security_id}"
        if record is None else None
    )


def get_holding_by_account_id_and_symbol(db, account_id: int, symbol: str) -> ActionResponse:
    """
    Gets a Holding for a given Account and Security record
    """
    with db.get_session() as session:
        holding = session.query(Holding).where(and_(
            Holding.account_id == account_id,
            Holding.symbol == symbol
        )).first()

    return ActionResponse(
        success=holding is not None,
        data=holding,
        message=f"No holding found for account with ID {account_id} and security with ID {symbol}"
        if holding is None else None
    )



def get_holding_balances_by_holding_id(db, profile_id: int, holding_id: int) -> ActionResponse:
    """
    Returns all balances for a given holding by it's ID
    """
    with db.get_session() as session:
        balances = session.query(HoldingBalance)\
            .options(lazyload(HoldingBalance.holding)\
                .lazyload(Holding.account))\
            .where(and_(
                HoldingBalance.holding_id == holding_id,
                Holding.account_id == Account.id,
                Account.profile_id == profile_id
            )).all()
    return ActionResponse(
        success=balances is not None,
        data=balances,
        message=f"Could not find holding balances for holding with ID {holding_id}" if balances is None else None
    )


def create_holding(db, profile_id: int, account_id: int, request: CreateHoldingSchema) -> ActionResponse:
    """
    Creates a holding object in the given database and returns it
    """
    verification_result = _verify_holding_ownership(db, profile_id, account_id)
    if not verification_result.success:
        return verification_result

    holding = Holding()

    holding.account_id = account_id
    holding.security_symbol = request['security_symbol']
    holding.cost_basis = request['cost_basis']
    holding.quantity = request['quantity']
    holding.iso_currency_code = request['iso_currency_code']
    holding.timestamp = datetime.now(tz=timezone.utc)

    with db.get_session() as session:
        session.add(holding)
        session.commit()

    return ActionResponse(
        success=True,
        data=holding
    )


def update_holding(db, profile_id: int, request: UpdateHoldingSchema) -> ActionResponse:
    """
    Updates an existing holding object in the database with the details
    """
    holding_result = get_holding_by_id(db, profile_id, request['id'])
    if not holding_result.success or holding_result.data is None:
        return holding_result

    holding = holding_result.data

    holding.cost_basis = request['cost_basis']
    holding.quantity = request['quantity']
    holding.iso_currency_code = request['iso_currency_code']
    holding.timestamp = datetime.now(tz=timezone.utc)

    with db.get_session() as session:
        session.add(holding)
        session.commit()

    return ActionResponse(
        success=True,
        data=holding
    )


def delete_holding(db, profile_id: int, holding_id: int) -> ActionResponse:
    """
    Deletes an existing holding from the DB
    """
    holding_result = get_holding_by_id(db, profile_id, holding_id)
    if not holding_result.success or holding_result.data is None:
        return holding_result

    holding = holding_result.data

    verification_result = _verify_holding_ownership(db, profile_id, holding.account_id)
    if not verification_result.success:
        return verification_result

    with db.get_session() as session:
        session.delete(holding)
        session.commit()

    return ActionResponse(success=True)


def create_holding_balance(db, profile_id: int, request: CreateHoldingBalanceSchema) -> ActionResponse:
    """
    Creates a balance entry for a Holding record in the database
    """
    holding_result = get_holding_by_id(db, profile_id, request['holding_id'])
    if not holding_result.success or holding_result.data is None:
        return holding_result

    holding = holding_result.data

    verification_result = _verify_holding_ownership(db, profile_id, holding.account_id)
    if not verification_result.success:
        return verification_result

    holding_balance = HoldingBalance()

    holding_balance.holding_id = request['holding_id']
    holding_balance.cost_basis = request['cost_basis']
    holding_balance.quantity = request['quantity']
    holding_balance.timestamp = datetime.now(tz=timezone.utc)

    with db.get_session() as session:
        session.add(holding_balance)
        session.commit()

    return ActionResponse(
        success=True,
        data=holding_balance
    )

def create_holding(db, request: CreateHoldingSchema) -> ActionResponse:
    holding = Holding()

    holding.account_id = request['account.id']
    holding.security_id = request['security.id']
    holding.cost_basis = request['cost_basis']
    holding.quantity = request['quantity']
    holding.iso_currency_code = request['iso_currency_code']
    holding.timestamp = datetime.utcnow()

    with db.get_session() as session:
        session.add(holding)
        session.commit()

    return ActionResponse(
        success=True,
        data=holding
    )


def update_holding_balance(db, request: UpdateHoldingSchema) -> ActionResponse:
    holding_balance = HoldingBalance()

    holding_balance.holding_id = request['holding.id']
    holding_balance.cost_basis = request['cost_basis']
    holding_balance.quantity = request['quantity']
    holding_balance.timestamp = datetime.utcnow()

    with db.get_session() as session:
        session.add(holding_balance)
        session.commit()

    return ActionResponse(
        success=True,
        data=holding_balance
    )


def create_investment_transaction(db, request: CreateInvestmentTransactionSchema) -> ActionResponse:
    investment_transaction = InvestmentTransaction()

    investment_transaction.account_id = request['account.id']
    investment_transaction.name = request['name']
    investment_transaction.quantity = request['quantity']
    investment_transaction.price = sanitize_float(request['price'])
    investment_transaction.fees = sanitize_float(request['fees'])
    investment_transaction.amount = sanitize_float(request['amount'])
    investment_transaction.date = request['date']
    investment_transaction.iso_currency_code = request['iso_currency_code']
    investment_transaction.type = request['type']
    investment_transaction.subtype = request['subtype']
    investment_transaction.investment_transaction_id = request['investment_transaction_id']
    investment_transaction.timestamp = datetime.utcnow()

    with db.get_session() as session:
        session.add(investment_transaction)
        session.commit()

    return ActionResponse(
        success=True,
        data=investment_transaction
    )


def _verify_holding_ownership(db, profile_id, account_id):
    account_result = get_account_by_id(db, profile_id, account_id)

    if not account_result.success or account_result.data is None:
        return account_result

    if not account_result.data.profile_id == profile_id:
        return ActionResponse(
            success=False,
            message=f"Can't create entity for that account - it doesn't belong to the requested profile"
        )

    return account_result
