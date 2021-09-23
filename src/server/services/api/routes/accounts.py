from flask import Blueprint, request
from datetime import datetime

from core.repositories.security_repository import get_repository as get_security_repository
from core.repositories.account_repository import get_repository as get_account_repository, GetAccountBalanceRequest
from core.apis.plaid.oauth import PlaidApiConfig
from core.apis.mailgun import MailGunConfig

from server.services.api.routes.decorators import authed, get_identity

from server.config import config as server_config
from server.services.api import load_config
app_config = load_config()

mysql_config = app_config['db']
iex_config = app_config['iexcloud']

# define a plaid oauth client config
plaid_config = PlaidApiConfig()
plaid_config.env = app_config['plaid']['env']
plaid_config.client_id = app_config['plaid']['client_id']
plaid_config.secret = app_config['plaid']['secret']

mailgun_config = MailGunConfig(
    domain=server_config['mailgun']['domain'],
    api_key=server_config['mailgun']['api_key']
)


# define the blueprint for plaid oauth
account_bp = Blueprint('account', __name__)


@account_bp.route('/v1/api/accounts', methods=['GET'])
@authed
def list_accounts():
    user = get_identity()
    repo = get_account_repository(mysql_config=mysql_config, plaid_config=plaid_config,
                                  mailgun_config=mailgun_config, iex_config=iex_config)
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
    repo = get_account_repository(mysql_config=mysql_config, plaid_config=plaid_config,
                                  mailgun_config=mailgun_config, iex_config=iex_config)
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
    repo = get_account_repository(mysql_config=mysql_config, plaid_config=plaid_config,
                                  mailgun_config=mailgun_config, iex_config=iex_config)
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


@account_bp.route('/v1/api/accounts/<account_id>/holdings', methods=['GET'])
@authed
def list_holdings(account_id):
    profile = get_identity()
    repository = get_security_repository(mysql_config=mysql_config, plaid_config=plaid_config)
    holdings = repository.get_holdings_by_profile_and_account(profile_id=profile['id'], account_id=account_id)
    if holdings is not None:
        return {
            'success': True,
            'data': [h.to_dict() for h in holdings]
        }
    return {
        'success': False
    }
