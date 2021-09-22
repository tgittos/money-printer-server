import traceback
from datetime import date, timedelta

from plaid import ApiException
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from plaid.model.investments_transactions_get_request import InvestmentsTransactionsGetRequest
from plaid.model.investments_transactions_get_request_options import InvestmentsTransactionsGetRequestOptions

from core.lib.logger import get_logger
from core.apis.plaid.common import get_plaid_api_client


class InvestmentsConfig(object):
    plaid_config = None

    def __init__(self, plaid_config):
        self.plaid_config = plaid_config


class Investments:
    def __init__(self, accounts_config=None):
        self.logger = get_logger(__name__)
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
            self.logger.exception("unexpected error from upstream provider fetching account holdings for account: {0}"
                                  .format(traceback.format_exc()))
            return

    def get_transactions(self, access_token, start=None, end=None):
        try:
            if start is None:
                start = date.today()
            if end is None:
                end = start - timedelta(days=365)

            transactions = []

            request = InvestmentsTransactionsGetRequest(
                access_token=access_token,
                start_date=start,
                end_date=end,
                options=InvestmentsTransactionsGetRequestOptions()
            )

            response = self.client.investments_transactions_get(request)
            transactions.extend(response['transactions'])

            investment_transactions = response['investment_transactions']

            while len(investment_transactions) < response['total_investment_transactions']:
                request = InvestmentsTransactionsGetRequest(
                    access_token=access_token,
                    start_date='2019-03-01',
                    end_date='2010-04-30',
                    options=InvestmentsTransactionsGetRequestOptions(
                        offset=len(transactions)
                    )
                )
                response = self.client.investments_transactions_get(request)
                transactions.extend(response['transactions'].to_dict)

            return {
                'transactions': transactions
            }

        except ApiException as e:
            self.logger.exception("unexepcted error from upstream provider fetching account transactions for account: {0}"
                                  .format(traceback.format_exc()))
            return
