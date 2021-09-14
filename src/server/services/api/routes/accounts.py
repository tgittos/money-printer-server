from flask import Blueprint, request
from datetime import datetime

from core.apis.plaid.common import PlaidApiConfig
from core.repositories.account_repository import AccountRepository, get_repository as get_account_repository, GetAccountBalanceRequest

from server.services.api.routes.decorators import authed, get_identity


# define the blueprint for plaid oauth
account_bp = Blueprint('account', __name__)


@account_bp.route('/v1/api/accounts', methods=['GET'])
@authed
def list_accounts():
    user = get_identity()
    repo = get_account_repository()
    if user is not None and user['id'] is not None:
        accounts = repo.get_all_accounts_by_profile(user['id'])
        if accounts is not None:
            return {
                'success': True,
                'data': [a.to_dict() for a in accounts]
            }
    return {
        'success': False
    }


@account_bp.route('/v1/api/accounts/<account_id>/sync', methods=['GET'])
@authed
def request_account_sync(account_id):
    user = get_identity()
    repo = get_account_repository()
    if user is not None and user['id'] is not None:
        account = repo.get_account_by_account_id(int(account_id))
        repo.schedule_account_sync(account.profile_id, account.plaid_item_id)
        return {
            'success': True
        }
    return {
        'success': False
    }


@account_bp.route('/v1/api/accounts/<account_id>/balances', methods=['GET'])
@authed
def request_account_balances(account_id):
    user = get_identity()
    repo = get_account_repository()
    start_qs = request.args.get('start')
    start = None
    end_qs = request.args.get('end')
    end = None
    if start_qs is not None:
        start = datetime.fromtimestamp(start_qs)
    if end_qs is not None:
        end = datetime.fromtimestamp(end_qs)
    if user is not None and user['id'] is not None:
        balances = repo.get_account_balances(GetAccountBalanceRequest(
            profile_id=user['id'],
            account_id=account_id,
            start=start,
            end=end
        ))
        if balances is not None:
            return {
                'success': True,
                'data': [b.to_dict() for b in balances]
            }
