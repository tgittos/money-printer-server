from flask import Blueprint
from flask import request

from core.apis.plaid.oauth import PlaidOauth, PlaidOauthConfig
from core.repositories.account_repository import AccountRepository
from .decorators import authed, get_identity
from config import mysql_config, plaid_config, mailgun_config, iex_config

from api.lib.constants import API_PREFIX

oauth_config = PlaidOauthConfig(
    mysql_config=mysql_config,
    plaid_config=plaid_config
)

# define the blueprint for plaid oauth
oauth_bp = Blueprint('plaid_oauth', __name__)


@oauth_bp.route(f"/{API_PREFIX}/plaid/info", methods=['GET'])
@authed
def info():
    client = PlaidOauth(oauth_config)
    result_json = client.info()
    return {
        'success': result_json is not None,
        'data': result_json
    }


@oauth_bp.route(f"/{API_PREFIX}/plaid/create_link_token", methods=['POST'])
@authed
def create_link_token():
    base_url = request.base_url
    client = PlaidOauth(oauth_config)
    result_json = client.create_link_token(base_url)
    return {
        'success': result_json is not None,
        'data': result_json
    }


@oauth_bp.route(f"/{API_PREFIX}/plaid/set_access_token", methods=['POST'])
@authed
def get_access_token():
    profile = get_identity()
    public_token = request.json['public_token']
    client = PlaidOauth(oauth_config)
    plaid_item = client.get_access_token(profile['id'], public_token)
    account_repo = AccountRepository()
    account_repo.schedule_account_sync(plaid_item=plaid_item)
    return {
        'success': plaid_item is not None,
        'message': 'Fetching accounts'
    }
