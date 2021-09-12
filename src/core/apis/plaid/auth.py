import json
from plaid import ApiException
from plaid.model.auth_get_request import AuthGetRequest

from core.apis.plaid.common import get_plaid_api_client, PlaidApiConfig
from core.repositories.plaid_repository import PlaidRepository


class AuthConfig(object):
    plaid_config = PlaidApiConfig()


class Auth:
    def __init__(self, auth_config=None):
        self.config = auth_config or AuthConfig()
        self.client = get_plaid_api_client(self.config.plaid_config)

    def get_auth(self, access_token):
        try:
            request = AuthGetRequest(
                access_token=access_token
            )
            response = self.client.auth_get(request)
            return response.to_dict()
        except ApiException as e:
            return json.loads(e.body)
