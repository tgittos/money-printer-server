import json

from plaid import ApiException
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.accounts_balance_get_request_options import AccountsBalanceGetRequestOptions

from core.apis.plaid.common import get_plaid_api_client
from core.lib.logger import get_logger


class AccountsConfig(object):
    plaid_config = None

    def __init__(self, plaid_config):
        self.plaid_config = plaid_config


class Accounts:

    logger = get_logger(__name__)

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

    def get_account_balance(self, access_token: str, plaid_account_id: str):
        try:
            self.logger.debug("sending account balance get request for account id: {0}".format(plaid_account_id))
            request = AccountsBalanceGetRequest(
                access_token=access_token,
                options=AccountsBalanceGetRequestOptions(
                    account_ids=[plaid_account_id]
                ))
            response = self.client.accounts_balance_get(request)
            return response.to_dict()
        except ApiException as e:
            return json.loads(e.body)
