from flask import Blueprint
from flask import request

from core.apis.plaid import oauth as plaid_oauth

# load the env config
from server import load_config
server_config = load_config()

# define a plaid oauth client config
plaid_config = plaid_oauth.OauthConfig()
plaid_config.product_name = "Money Printer"
plaid_config.env = server_config['plaid']['env']
plaid_config.client_id = server_config['plaid']['client_id']
plaid_config.secret = server_config['plaid']['secret']
plaid_config.mysql_config = server_config['db']

# define the blueprint for plaid oauth
oauth_bp = Blueprint('plaid_oauth', __name__)

@oauth_bp.route('/v1/api/plaid/info', methods=['POST'])
def info():
    client = plaid_oauth.Oauth(plaid_config)
    result_json = client.info()
    return result_json

@oauth_bp.route('/v1/api/plaid/create_link_token', methods=['POST'])
def create_link_token():
    client = plaid_oauth.Oauth(plaid_config)
    result_json = client.create_link_token()
    return result_json

@oauth_bp.route('/v1/api/plaid/set_access_token', methods=['POST'])
def get_access_token():
    global access_token
    global item_id
    public_token = request.form['public_token']
    client = plaid_oauth.Oauth(plaid_config)
    result_json = client.get_access_token(public_token)
    print("result_json: {0}".format(result_json))
    access_token = result_json['access_token']
    item_id = result_json['item_id']
    return result_json

@oauth_bp.route('/v1/api/plaid/auth', methods=['GET'])
def get_auth():
    client = plaid_oauth.Oauth(plaid_config)
    result_json = client.get_auth(access_token)
    return result_json
