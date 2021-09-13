import json

from plaid import ApiException
from plaid.model.accounts_get_request import AccountsGetRequest

from core.apis.plaid.common import get_plaid_api_client


class AccountsConfig(object):
    plaid_config = None

    def __init__(self, plaid_config):
        self.plaid_config = plaid_config


class Accounts:
    def __init__(self, accounts_config=None):
        self.config = accounts_config or AccountsConfig()
        self.client = get_plaid_api_client(self.config.plaid_config)

    def get_accounts(self, access_token):
        try:
            request = AccountsGetRequest(
                access_token=access_token
            )
            response = self.client.accounts_get(request)
            return response.to_dict()
        except ApiException as e:
            return json.loads(e.body)
