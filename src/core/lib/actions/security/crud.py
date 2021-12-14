from datetime import datetime
from sqlalchemy import and_

from core.models.profile import Profile
from core.models.account import Account
from core.models.security import Security
from core.models.holding import Holding
from core.models.holding_balance import HoldingBalance
from core.models.investment_transaction import InvestmentTransaction
from core.presentation.holding_presenters import HoldingWithSecurity, HoldingWithSecurityList, HoldingPresenter
from core.lib.types import SecurityList
from core.lib.utilities import sanitize_float

from .requests import CreateSecurityRequest, CreateHoldingRequest, CreateInvestmentTransactionRequest, \
    UpdateHoldingRequest


def get_securities(cls) -> SecurityList:
    r = cls.db.with_session(lambda session: session.query(Security).distinct(Security.ticker_symbol).all())
    return r


def get_security_by_symbol(cls, symbol: str) -> Security:
    r = cls.db.with_session(lambda session: session.query(Security).where(Security.ticker_symbol == symbol).first())
    return r


def get_securities_by_account(cls, account: Account) -> SecurityList:
    r = cls.db.with_session(lambda session: session.query(Security).where(Security.account_id == account.id).all())
    return r


def get_security_by_security_id(cls, plaid_security_id: str) -> Security:
    r = cls.db.with_session(lambda session: session.query(Security)
                            .where(Security.security_id == plaid_security_id).first())
    return r


def get_holdings_by_profile_and_account(cls, profile: Profile, account: Account) -> HoldingWithSecurityList:
    account = cls.db.with_session(lambda session: session.query(Account)
                                  .where(and_(
                                      Account.profile_id == profile.id,
                                      Account.id == account.id,
                                      )).first()
                                  )
    holdings = cls.db.with_session(lambda session: session.query(Holding).where(Holding.account_id == account.id).all())
    security_ids = list([h.security_id for h in holdings])
    securities = cls.db.with_session(lambda session: session.query(Security).filter(Security.id.in_(security_ids)).all())
    presentations = []
    presenter = HoldingPresenter(cls.db)
    for holding in holdings:
        security = list(filter(lambda s: s.id == holding.security_id, securities))[0]
        if security is None:
            presentations.append(HoldingWithSecurity(holding=holding, ticker='', price=0))
        else:
            presentations += presenter.with_balances(security=security, holdings=[holding])
    return presentations


def get_holding_by_plaid_account_id_and_plaid_security_id(cls, plaid_account_id: str,
                                                          plaid_security_id: str) -> Holding:
    """
    Gets a Holding for a Plaid account ID and Plaid security ID
    """
    account = cls.db.with_session(lambda session: session.query(Account)
                                  .where(Account.account_id == plaid_account_id).first())
    security = get_security_by_security_id(cls, plaid_security_id)
    record = cls.db.with_session(lambda session: session.query(Holding)
                                 .where(and_(
                                     Holding.account_id == account.id,
                                     Holding.security_id == security.id
                                 )).first()
                                 )
    return record


def get_holding_by_account_and_security(cls, account: Account, security: Security) -> Holding:
    """
    Gets a Holding for a given Account and Security record
    """
    r = cls.db.with_session(lambda session: session.query(Holding)
                            .where(and_(
                                Holding.account_id == account.id,
                                Holding.security_id == security.id
                            )).first()
                            )
    return r


def create_security(cls, request: CreateSecurityRequest) -> Security:
    security = Security()

    security.profile_id = request.profile.id
    security.account_id = request.account.id
    security.name = request.name
    security.ticker_symbol = request.ticker_symbol
    security.iso_currency_code = request.iso_currency_code
    security.institution_security_id = request.institution_security_id
    security.security_id = request.security_id
    security.proxy_security_id = request.proxy_security_id
    security.cusip = request.cusip
    security.isin = request.isin
    security.sedol = request.sedol
    security.timestamp = datetime.utcnow()

    def create(session):
        session.add(security)
        session.commit()

    cls.db.with_session(create)

    return security


def create_holding(cls, request: CreateHoldingRequest) -> Holding:
    holding = Holding()

    holding.account_id = request.account.id
    holding.security_id = request.security.id
    holding.cost_basis = request.cost_basis
    holding.quantity = request.quantity
    holding.iso_currency_code = request.iso_currency_code
    holding.timestamp = datetime.utcnow()

    def create(session):
        session.add(holding)
        session.commit()

    cls.db.with_session(create)

    return holding


def update_holding_balance(cls, request: UpdateHoldingRequest) -> HoldingBalance:
    holding_balance = HoldingBalance()

    holding_balance.holding_id = request.holding.id
    holding_balance.cost_basis = request.cost_basis
    holding_balance.quantity = request.quantity
    holding_balance.timestamp = datetime.utcnow()

    def create(session):
        session.add(holding_balance)
        session.commit()

    cls.db.with_session(create)

    return holding_balance


def create_investment_transaction(cls, request: CreateInvestmentTransactionRequest) -> InvestmentTransaction:
    investment_transaction = InvestmentTransaction()

    investment_transaction.account_id = request.account.id
    investment_transaction.name = request.name
    investment_transaction.quantity = request.quantity
    investment_transaction.price = sanitize_float(request.price)
    investment_transaction.fees = sanitize_float(request.fees)
    investment_transaction.amount = sanitize_float(request.amount)
    investment_transaction.date = request.date
    investment_transaction.iso_currency_code = request.iso_currency_code
    investment_transaction.type = request.type
    investment_transaction.subtype = request.subtype
    investment_transaction.investment_transaction_id = request.investment_transaction_id
    investment_transaction.timestamp = datetime.utcnow()

    def create(session):
        session.add(investment_transaction)
        session.commit()

    cls.db.with_session(create)

    return investment_transaction
