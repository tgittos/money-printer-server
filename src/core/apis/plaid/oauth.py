import time

from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

from core.apis.plaid.common import get_plaid_api_client, PlaidApiConfig, PLAID_PRODUCTS_STRINGS, PLAID_PRODUCTS
from core.repositories.plaid_repository import PlaidRepository, CreatePlaidItem


class OauthConfig:
    def __init__(self, plaid_config, mysql_config):
        self.plaid_config = PlaidApiConfig()
        self.plaid_config.env = plaid_config['env']
        self.plaid_config.secret = plaid_config['secret']
        self.plaid_config.client_id = plaid_config['client_id']
        self.mysql_config = mysql_config


class Oauth:

    def __init__(self, oauth_config):
        self.config = oauth_config
        self.client = get_plaid_api_client(self.config.plaid_config)
        self.repository = PlaidRepository()

    def info(self):
        return {
            'item_id': '',
            'access_token': '',
            'products': PLAID_PRODUCTS_STRINGS
        }

    def create_link_token(self, webhook_url):
        plaid_config = self.config.plaid_config
        request = LinkTokenCreateRequest(
            products=PLAID_PRODUCTS,
            client_name=plaid_config.product_name,
            country_codes=plaid_config.country_codes,
            language=plaid_config.language,
            webhook=webhook_url,
            user=LinkTokenCreateRequestUser(
                client_user_id=str(time.time())
            )
        )

        response = self.client.link_token_create(request)
        return response.to_dict()

    def get_access_token(self, profile_id, public_token):
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token
        )
        exchange_response = self.client.item_public_token_exchange(exchange_request)
        access_token = exchange_response['access_token']
        item_id = exchange_response['item_id']
        request_id = exchange_response['request_id']
        plaid_item = self.__store_link(profile_id, request_id, item_id, access_token)
        return plaid_item

    def __store_link(self, profile, request_id, item_id, access_token):
        plaid_item = self.repository.create_plaid_item(CreatePlaidItem(
            profile=profile,
            item_id=item_id,
            access_token=access_token,
            request_id=request_id
        ))
        return plaid_item

    def __fetch_link(self, item_id):
        self.repository.get_plaid_item_by_plaid_item_id(id=item_id)
