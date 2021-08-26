import time
import json

from plaid import ApiException
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

from core.apis.plaid.common import get_plaid_api_client, PlaidApiConfig, PLAID_PRODUCTS_STRINGS, PLAID_PRODUCTS
from core.repositories.plaid_repository import PlaidRepository, CreatePlaidItem, GetPlaidItem


class OauthConfig(object):
    plaid_config = PlaidApiConfig()
    mysql_config = None


class Oauth:

    def __init__(self, oauth_config):
        self.config = oauth_config
        self.client = get_plaid_api_client(self.config.plaid_config)
        self.repository = PlaidRepository(self.config.mysql_config)

    def info(self):
        return {
            'item_id': '',
            'access_token': '',
            'products': PLAID_PRODUCTS_STRINGS
        }

    def create_link_token(self):
        try:
            plaid_config = self.config.plaid_config
            print("client_id: {0}, secret: {1}".format(plaid_config.client_id, plaid_config.secret))
            request = LinkTokenCreateRequest(
                products=PLAID_PRODUCTS,
                client_name=plaid_config.product_name,
                country_codes=plaid_config.country_codes,
                language=plaid_config.language,
                user=LinkTokenCreateRequestUser(
                    client_user_id=str(time.time())
                )
            )

            response = self.client.link_token_create(request)
            return response.to_dict()
        except ApiException as e:
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
        except ApiException as e:
            return json.loads(e.body)


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
