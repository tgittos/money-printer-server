import json

from flask import Blueprint
from flask import request

from core.apis.plaid.common import PlaidApiConfig
from core.apis.plaid.oauth import Oauth, OauthConfig
from core.apis.plaid.auth import Auth, AuthConfig
from server.services.api.routes.decorators import authed
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
    return result_json

@oauth_bp.route('/v1/api/plaid/create_link_token', methods=['POST'])
@authed
def create_link_token():
    client = Oauth(oauth_config)
    result_json = client.create_link_token()
    return result_json

@oauth_bp.route('/v1/api/plaid/set_access_token', methods=['POST'])
@authed
def get_access_token():
    public_token = request.json['public_token']
    client = Oauth(oauth_config)
    account = client.get_access_token(public_token)
    return {
        'success': account is not None,
        'data': account
    }

@oauth_bp.route('/v1/api/plaid/auth', methods=['GET'])
@authed
def get_auth():
    client = Auth(auth_config)
    result_json = client.get_auth(access_token)
    return result_json
