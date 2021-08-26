import time
# todo - get rid of this - should be out on the API not in the core
from flask import jsonify
import json

import plaid
from plaid.api import plaid_api
from plaid.model.country_code import CountryCode
from plaid.model.products import Products
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.auth_get_request import AuthGetRequest
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

from core.repositories.plaid_repository import PlaidRepository, CreatePlaidItem, GetPlaidItem

PLAID_PRODUCTS_STRINGS = ["assets", "transactions"]
PLAID_DEFAULT_COUNTRY_CODES = ["US"]
PLAID_DEFAULT_LANGUAGE = "en"
PLAID_PRODUCTS = list(map(lambda x: Products(x), PLAID_PRODUCTS_STRINGS))
PLAID_COUNTRY_CODES = list(map(lambda x: CountryCode(x), PLAID_DEFAULT_COUNTRY_CODES))


class OauthConfig(object):
    env = "sandbox"
    product_name = "Money Printer"
    country_codes = PLAID_COUNTRY_CODES
    language = PLAID_DEFAULT_LANGUAGE
    client_id = None
    secret = None
    version = "2020-09-14"
    mysql_config = None


class Oauth:

    def __init__(self, oauth_config):
        self.config = oauth_config
        api_client = plaid.ApiClient(plaid.Configuration(
            host=self.__get_host(),
            api_key={
                'clientId': self.config.client_id,
                'secret': self.config.secret,
                'plaidVersion': self.config.version
            }
        ))
        self.client = plaid_api.PlaidApi(api_client)
        self.repository = PlaidRepository(self.config.mysql_config)

    def info(self):
        return jsonify({
            'item_id': '',
            'access_token': '',
            'products': PLAID_PRODUCTS_STRINGS
        })

    def create_link_token(self):
        try:
            print("client_id: {0}, secret: {1}".format(self.config.client_id, self.config.secret))
            request = LinkTokenCreateRequest(
                products=PLAID_PRODUCTS,
                client_name=self.config.product_name,
                country_codes=self.config.country_codes,
                language=self.config.language,
                user=LinkTokenCreateRequestUser(
                    client_user_id=str(time.time())
                )
            )

            response = self.client.link_token_create(request)
            return response.to_dict()
        except plaid.ApiException as e:
            return json.loads(e.body)

    def get_access_token(self, public_token):
        try:
            exchange_request = ItemPublicTokenExchangeRequest(
                public_token=public_token
            )
            exchange_response = self.client.item_public_token_exchange(exchange_request)
            access_token = exchange_response['access_token']
            item_id = exchange_response['item_id']
            request_id = exchange_response['request_id']
            self.__store_link(request_id, item_id, access_token)
            return exchange_response.to_dict()
        except plaid.ApiException as e:
            return json.loads(e.body)

    def get_auth(self, access_token):
        try:
            request = AuthGetRequest(
                access_token=access_token
            )
            response = self.client.auth_get(request)
            return response.to_dict()
        except plaid.ApiException as e:
            error_response = self.__format_error(e)
            return jsonify(error_response)

    def __get_host(self):
        if self.config.env == 'production':
            return plaid.Environment.Production
        elif self.config.env == 'development':
            return plaid.Environment.Development

        return plaid.Environment.Sandbox

    def __format_error(self, e):
        response = json.loads(e.body)
        return {'error': {'status_code': e.status, 'display_message':
            response['error_message'], 'error_code': response['error_code'], 'error_type': response['error_type']}}

    def __store_link(self, request_id, item_id, access_token):
        self.repository.create_plaid_item(CreatePlaidItem(
            item_id=item_id,
            access_token=access_token,
            request_id=request_id
        ))

    def __fetch_link(self, item_id):
        self.repository.get_plaid_item(GetPlaidItem(
            item_id=item_id
        ))
