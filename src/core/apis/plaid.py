import sys
sys.path.append('./../../src')

from os import path
from datetime import date, datetime, timedelta
import time
import calendar
import finnhub
import pandas

import plaid
from plaid.api import plaid_api
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser

from urllib3.exceptions import ReadTimeoutError

import config
import core.lib.constants

class Plaid:
    
    def __init__(self):
        api_client = plaid.ApiClient(plaid.Configuration(
            host=__get_host(),
            api_key = {
                'clientId': config.api_keys.plaid.client_id,
                'secret': config.api_keys.plaid.secret,
                'plaidVersion': config.api_keys.plaid.version
            }
        ))
        self.client = plaid_api.PlaidApi(api_client)
    
    def create_link_token():
        try:
            request = LinkTokenCreateRequest(
                products = ,
                client_name = constants.PRODUCT_NAME,
                country_codes=config.plaid.country_codes,
                language = constants.LANGUAGE,
                user = LinkTokenCreateRequestUser(
                    client_user_id=str(time.time())
                )
            )
            
            response = self.client.link_token_create(request)
            return jsonify(response.to_dict())
        except plaid.ApiException as e:
            return json.loads(e.body)
        
    def get_access_token(public_token):
        try:
            exchange_request = ItemPublicTokenExchangeRequest(
                public_token = public_token
            )
            exchange_response = client.item_public_token_exchange(exchange_request)
            access_token = exchange_response['access_token']
            item_id = exchange_response['item_id']
            return jsonify(exchange_response.to_dict())
        except plaid.ApiException as e:
            return json.loads(e.body)
    
    def get_auth(access_token):
        try:
            request = AuthGetRequest(
                access_token = access_token
            )
            response = client.auth_get(request)
            return jsonify(response.to_dict())
        except plaid.ApiException as e:
            error_response = format_error(e)
            return jsonify(error_response)
    
    def __get_host(self):
        if config.plaid.env == 'production':
            return plaid.Environment.Production
        elif config.plaid.env == 'development':
            return plaid.Environment.Development
        
        return plaid.Environment.Sandbox
            