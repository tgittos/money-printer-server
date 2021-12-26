from datetime import datetime
from sqlalchemy import and_

from core.models.profile import Profile
from core.models.account import Account
from core.models.security import Security
from core.models.holding import Holding
from core.models.holding_balance import HoldingBalance
from core.models.investment_transaction import InvestmentTransaction
from core.lib.utilities import sanitize_float
from core.actions.action_response import ActionResponse
from core.schemas.security_schemas import CreateSecuritySchema
from core.schemas.holding_schemas import CreateHoldingSchema, UpdateHoldingSchema
from core.schemas.investment_schemas import CreateInvestmentTransactionSchema


def get_securities(db) -> ActionResponse:
    with db.get_session() as session:
        securities = session.query(Security).distinct(
            Security.ticker_symbol).all()

    return ActionResponse(
        success=securities is not None,
        data=securities,
        message=f"No securities found" if securities is None else None
    )


def get_security_by_symbol(db, symbol: str) -> ActionResponse:
    with db.get_session() as session:
        security = session.query(Security).where(
            Security.ticker_symbol == symbol).first()

    return ActionResponse(
        success=security is not None,
        data=security,
        message=f"Security with symbol ${symbol} not found" if security is None else None
    )


def get_securities_by_account(db, account: Account) -> ActionResponse:
    with db.get_session() as session:
        securities = session.query(Security).where(
            Security.account_id == account.id).all()

    return ActionResponse(
        success=securities is not None,
        data=securities,
        message=f"No securities found for account with ID ${account.id}" if securities is None else None
    )


def get_security_by_security_id(db, plaid_security_id: str) -> ActionResponse:
    with db.get_session() as session:
        security = session.query(Security).where(
            Security.security_id == plaid_security_id).first()

    return ActionResponse(
        success=security is not None,
        data=security,
        message=f"Security not found for plaid_security_id ${plaid_security_id}" if security is None else None
    )


def get_holdings_by_profile_and_account(db, profile: Profile, account: Account) -> ActionResponse:
    # TODO - I need to re-write this SQL to pull in the holdings and the attached securities
    # and return that for schema dumping
    with db.get_session() as session:
        account = session.query(Account).where(and_(
            Account.profile_id == profile.id,
            Account.id == account.id,
        )).first()
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
    security = get_security_by_security_id(db, plaid_security_id)
    with db.get_session() as session:
        account = session.query(Account).where(
            Account.account_id == plaid_account_id).first()
        record = session.query(Holding).where(and_(
            Holding.account_id == account.id,
            Holding.security_id == security.id
        )).first()

    return ActionResponse(
        success=record is not None,
        data=record,
        message=f"No holding found for plaid_account_id {plaid_account_id} and plaid_security_id {plaid_security_id}"
        if record is None else None
    )


def get_holding_by_account_and_security(db, account: Account, security: Security) -> ActionResponse:
    """
    Gets a Holding for a given Account and Security record
    """
    with db.get_session() as session:
        holding = session.query(Holding).where(and_(
            Holding.account_id == account.id,
            Holding.security_id == security.id
        )).first()

    return ActionResponse(
        success=holding is not None,
        data=holding,
        message=f"No holding found for account with ID {account.id} and security with ID {security.id}"
        if holding is None else None
    )


def create_security(db, request: CreateSecuritySchema) -> ActionResponse:
    security = Security()

    security.profile_id = request['profile.id']
    security.account_id = request['account.id']
    security.name = request['name']
    security.ticker_symbol = request['ticker_symbol']
    security.iso_currency_code = request['iso_currency_code']
    security.institution_security_id = request['institution_security_id']
    security.security_id = request['security_id']
    security.proxy_security_id = request['proxy_security_id']
    security.cusip = request['cusip']
    security.isin = request['isin']
    security.sedol = request['sedol']
    security.timestamp = datetime.utcnow()

    with db.get_session() as session:
        session.add(security)
        session.commit()

    return ActionResponse(
        success=True,
        data=security
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