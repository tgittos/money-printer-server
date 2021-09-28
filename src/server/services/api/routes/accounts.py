from flask import Blueprint, request, abort
from datetime import datetime

from core.repositories.profile_repository import ProfileRepository
from core.repositories.account_repository import AccountRepository
from core.repositories.balance_repository import BalanceRepository, GetAccountBalanceRequest
from core.repositories.security_repository import SecurityRepository
from config import env
from .decorators import authed, get_identity


# define the blueprint for plaid oauth
account_bp = Blueprint('account', __name__)


@account_bp.route('/v1/api/accounts', methods=['GET'])
@authed
def list_accounts():
    user = get_identity()
    profile_repo = ProfileRepository()
    profile = profile_repo.get_profile_by_id(user['id'])
    account_repo = AccountRepository()
    accounts = account_repo.get_accounts_by_profile_with_balances(profile=profile)
    if accounts is not None:
        return {
            'success': True,
            'data': [a.to_dict() for a in accounts]
        }
    else:
        abort(404)


@account_bp.route('/v1/api/accounts/<account_id>/sync', methods=['POST'])
@authed
def request_account_sync(account_id: int):
    user = get_identity()
    profile_repo = ProfileRepository()
    profile = profile_repo.get_profile_by_id(user['id'])
    if profile is not None:
        account_repo = AccountRepository()
        account = account_repo.get_account_by_id(profile=profile, account_id=account_id)
        if account is None:
            abort(404)
        account_repo.schedule_account_sync(account)
        return {
            'success': True
        }
    else:
        abort(404)


@account_bp.route('/v1/api/accounts/<account_id>/balances', methods=['GET'])
@authed
def request_account_balances(account_id):
    user = get_identity()
    profile_repo = ProfileRepository()
    profile = profile_repo.get_profile_by_id(user['id'])
    account_repo = AccountRepository()
    accounts = account_repo.get_account_by_profile_with_balance(profile, account_id)
    if accounts is None:
        abort(404)
    return {
        'success': True,
        'data': [a.to_dict() for a in accounts]
    }


@account_bp.route('/v1/api/accounts/<account_id>/holdings', methods=['GET'])
@authed
def list_holdings(account_id):
    user = get_identity()
    profile_repo = ProfileRepository()
    account_repo = AccountRepository()
    profile = profile_repo.get_profile_by_id(user['id'])
    account = account_repo.get_account_by_id(profile=profile, account_id=account_id)
    if account is None:
        abort(404)
    security_repo = SecurityRepository()
    holdings = security_repo.get_holdings_by_profile_and_account(profile=profile, account=account)
    if holdings is None:
        abort(404)
    return {
        'success': True,
        'data': [h.to_dict() for h in holdings]
    }
