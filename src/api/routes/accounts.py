from flask import Blueprint, request, abort

from core.repositories.profile_repository import ProfileRepository
from core.repositories.account_repository import AccountRepository
from core.repositories.security_repository import SecurityRepository
from core.schemas import ReadAccountSchema, ReadAccountBalanceSchema, ReadHoldingSchema
from core.schemas.account_schemas import ReadAccountSchema
from core.schemas.holding_schemas import ReadHoldingSchema
from config import env
from .decorators import authed, get_identity

from api.lib.constants import API_PREFIX


# define the blueprint for plaid oauth
account_bp = Blueprint('account', __name__)


@account_bp.route(f"/{API_PREFIX}/accounts", methods=['GET'])
@authed
def list_accounts():
    """
    ---
    get:
        summary: Get a list of all accounts the belong to the signed in profile
        security:
            - jwt: []
        responses:
            200:
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                success:
                                    type: boolean
                                data:
                                    type: array
                                    items: ReadAccountSchema
        tags:
            - Account
    """
    user = get_identity()
    account_repo = AccountRepository()
    accounts = account_repo.get_accounts_by_profile_id(profile_id=user['id'])
    if accounts.success and accounts.data is not None:
        return { 
            'success': True,
            'data': ReadAccountSchema(
                many=True,
                exclude=("balances","profile", "transactions", "holdings", "plaid_item")
            ).dump(accounts.data)
        }
    else:
        abort(404)


@account_bp.route(f"/{API_PREFIX}/accounts/<account_id>/sync", methods=['POST'])
@authed
def request_account_sync(account_id: int):
    """
    ---
    post:
        summary: Schedule an immediate sync of specified account attached to the profile
        security:
            - jwt: []
        responses:
            200:
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                success:
                                    type: boolean
        tags:
            - Account
    """
    user = get_identity()
    account_repo = AccountRepository()
    result = account_repo.schedule_account_sync(user['id'], account_id)
    if result.success:
        return {
            'success': True
        }
    return {
        'success': False
    }, 400


@account_bp.route(f"/{API_PREFIX}/accounts/<account_id>/balances", methods=['GET'])
@authed
def request_account_balances(account_id):
    """
    ---
    get:
        summary: Get a historical list of account balances for a given account
        security:
            - jwt: []
        responses:
            200:
                description: Account balance object
                content:
                    application/json:
                        type: object
                        properties:
                            success:
                                type: boolean
                            data:
                                type: array
                                items: ReadAccountBalanceSchema
        tags:
            - Account
    """
    user = get_identity()
    account_repo = AccountRepository()
    balance_result = account_repo.get_balances_by_account_id(account_id)
    if not balance_result or balance_result is None:
        abort(404)
    return {
        'success': True,
        'data': ReadAccountBalanceSchema(
            many=True,
            exclude=("account",)
        ).dump(balance_result.data)
    }


@account_bp.route(f"/{API_PREFIX}/accounts/<account_id>/holdings", methods=['GET'])
@authed
def list_holdings(account_id):
    """
    ---
    get:
        summary: Get a list of investment holdings for a given account
        security:
            - jwt: []
        responses:
            200:
                description: Holding object
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                success:
                                    type: boolean
                                data:
                                    type: array
                                    items: ReadHoldingSchema
        tags:
            - Account
    """
    print('account_id:', account_id)
    user = get_identity()
    security_repo = SecurityRepository()
    print('user', user)
    holding_result = security_repo.get_holdings_by_profile_id_and_account_id(
        profile_id=user['id'], account_id=account_id)
    if not holding_result.success or holding_result.data is None:
        abort(404)
    return {
        'success': True,
        'data': ReadHoldingSchema(
            many=True,
            exclude=("account", "balances", "security")
        ).dump(holding_result.data)
    }
