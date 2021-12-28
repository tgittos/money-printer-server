import time
from os import environ

from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest

from core.apis.plaid.common import get_plaid_api_client, PlaidApiConfig

class PlaidOauth:

    def __init__(self):
        self.api_config = PlaidApiConfig() 
        self.client = get_plaid_api_client(self.api_config)

    def create_link_token(self, current_host):
        if 'MP_WEBHOOK_HOST' in environ:
            webhook_host = environ['MP_WEBHOOK_HOST']
        else:
            webhook_host =  current_host
        webhook_url = f"{webhook_host}/v1/webhooks/plaid"
        request = LinkTokenCreateRequest(
            products=self.api_config.products,
            client_name=self.api_config.product_name,
            country_codes=self.api_config.country_codes,
            language=self.api_config.language,
            webhook=webhook_url,
            user=LinkTokenCreateRequestUser(
                client_user_id=str(time.time())
            )
        )

        response = self.client.link_token_create(request)
        return response.to_dict()

    def get_access_token(self, public_token):
        exchange_request = ItemPublicTokenExchangeRequest(
            public_token=public_token
        )
        exchange_response = self.client.item_public_token_exchange(
            exchange_request)
        return exchange_response
