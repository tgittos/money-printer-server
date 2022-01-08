from datetime import datetime
from sqlalchemy import and_

from core.lib.utilities import sanitize_float
from core.actions.action_response import ActionResponse

from stonk_server.schemas import CreateSecuritySchema
from stonk_server.models import Security

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


def get_securities_by_account_id(db, profile_id: int, account_id: int) -> ActionResponse:
    with db.get_session() as session:
        securities = session.query(Security).where(
            Security.account_id == account_id).all()

    return ActionResponse(
        success=securities is not None,
        data=securities,
        message=f"No securities found for account with ID ${account_id}" if securities is None else None
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
