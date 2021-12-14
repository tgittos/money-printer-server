from flask import Blueprint
from flask import request

from core.apis.plaid.oauth import Oauth, OauthConfig
from core.repositories.account_repository import AccountRepository
from .decorators import authed, get_identity
from config import mysql_config, plaid_config, mailgun_config, iex_config

oauth_config = OauthConfig(
    mysql_config=mysql_config,
    plaid_config=plaid_config
)

# define the blueprint for plaid oauth
oauth_bp = Blueprint('plaid_oauth', __name__)


@oauth_bp.route('/v1/api/plaid/info', methods=['POST'])
@authed
def info():
    client = Oauth(oauth_config)
    result_json = client.info()
    return {
        'success': result_json is not None,
        'data': result_json
    }


@oauth_bp.route('/v1/api/plaid/create_link_token', methods=['POST'])
@authed
def create_link_token():
    base_url = request.base_url
    # webhook_url = base_url + "/v1/webhooks/plaid"
    # below is testing value only
    webhook_url = "http://6b654d2cf969.ngrok.io" + "/v1/webhooks/plaid"
    client = Oauth(oauth_config)
    result_json = client.create_link_token(webhook_url)
    return {
        'success': result_json is not None,
        'data': result_json
    }


@oauth_bp.route('/v1/api/plaid/set_access_token', methods=['POST'])
@authed
def get_access_token():
    profile = get_identity()
    public_token = request.json['public_token']
    client = Oauth(oauth_config)
    plaid_item = client.get_access_token(profile['id'], public_token)
    account_repo = AccountRepository()
    account_repo.schedule_account_sync(plaid_item=plaid_item)
    return {
        'success': plaid_item is not None,
        'message': 'Fetching accounts'
    }
