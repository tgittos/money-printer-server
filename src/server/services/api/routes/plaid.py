import json

from flask import Blueprint
from flask import request

from core.apis.plaid.common import PlaidApiConfig
from core.apis.plaid.oauth import Oauth, OauthConfig
from core.apis.plaid.auth import Auth, AuthConfig
from core.repositories.account_repository import get_repository as get_account_repository
from server.services.api.routes.decorators import authed, get_identity
from server.services.api import load_config

server_config = load_config()

# define a plaid oauth client config
plaid_config = PlaidApiConfig()
plaid_config.env = server_config['plaid']['env']
plaid_config.client_id = server_config['plaid']['client_id']
plaid_config.secret = server_config['plaid']['secret']

oauth_config = OauthConfig()
oauth_config.mysql_config = server_config['db']
oauth_config.plaid_config = plaid_config

auth_config = AuthConfig()
auth_config.mysql_config = server_config['db']
auth_config.plaid_config = plaid_config


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
    client = Oauth(oauth_config)
    result_json = client.create_link_token()
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
    account_repo = get_account_repository()
    account_repo.schedule_account_sync(profile['id'], plaid_item['id'])
    return {
        'success': plaid_item is not None,
        'message': 'Fetching accounts'
    }
