import json

from plaid import ApiException
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest

from core.apis.plaid.common import get_plaid_api_client


class InvestmentsConfig(object):
    plaid_config = None

    def __init__(self, plaid_config):
        self.plaid_config = plaid_config


class Investments:
    def __init__(self, accounts_config=None):
        self.config = accounts_config or InvestmentsConfig()
        self.client = get_plaid_api_client(self.config.plaid_config)

    def get_investments(self, access_token):
        try:
            request = InvestmentsHoldingsGetRequest(
                access_token=access_token
            )
            response = self.client.investments_holdings_get(request)
            return response.to_dict()
        except ApiException as e:
            return json.loads(e.body)
