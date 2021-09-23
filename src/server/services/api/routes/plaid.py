import json

from flask import Blueprint
from flask import request

from core.apis.plaid.common import PlaidApiConfig
from core.apis.plaid.oauth import Oauth, OauthConfig
from core.apis.mailgun import MailGunConfig
from core.repositories.account_repository import get_repository as get_account_repository
from server.services.api.routes.decorators import authed, get_identity
from server.services.api import load_config

from server.config import config as server_config
app_config = load_config()

# define a plaid oauth client config
plaid_config = PlaidApiConfig()
plaid_config.env = app_config['plaid']['env']
plaid_config.client_id = app_config['plaid']['client_id']
plaid_config.secret = app_config['plaid']['secret']

oauth_config = OauthConfig()
oauth_config.mysql_config = app_config['db']
oauth_config.plaid_config = plaid_config

mailgun_config = MailGunConfig(
    api_key=server_config['mailgun']['api_key'],
    domain=server_config['mailgun']['domain']
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
    account_repo = get_account_repository(mysql_config=app_config['db'], plaid_config=plaid_config,
                                          mailgun_config=mailgun_config)
    account_repo.schedule_account_sync(plaid_item_id=plaid_item.id)
    return {
        'success': plaid_item is not None,
        'message': 'Fetching accounts'
    }
