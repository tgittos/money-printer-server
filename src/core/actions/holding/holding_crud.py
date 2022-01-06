from sqlalchemy import and_
from sqlalchemy.orm import selectinload, lazyload
from datetime import datetime, timezone

from core.models import Holding, HoldingBalance, Security, Account
from core.schemas import CreateHoldingSchema, UpdateHoldingSchema, CreateHoldingBalanceSchema, UpdateHoldingBalanceSchema
from core.actions.action_response import ActionResponse
from core.actions.account.crud import get_account_by_id


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
