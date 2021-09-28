from datetime import datetime, date, timedelta

from core.stores.mysql import MySql
from core.apis.plaid.investments import Investments, InvestmentsConfig
from core.models.plaid_item import PlaidItem
from core.models.profile import Profile
from core.models.account import Account
from core.models.investment_transaction import InvestmentTransaction
from core.lib.logger import get_logger
from config import mysql_config, plaid_config

from .facets.plaid.crud import get_plaid_item_by_id
from .facets.security.crud import create_security, create_holding, create_investment_transaction,\
    get_security_by_security_id, get_holdings_by_profile_and_account, update_holding_balance,\
    get_holding_by_plaid_account_id_and_plaid_security_id, get_security_by_symbol, get_securities_by_account,\
    get_securities
from .facets.security.requests import CreateSecurityRequest, CreateHoldingRequest, CreateInvestmentTransactionRequest,\
    UpdateHoldingRequest


class SecurityRepository:

    logger = get_logger(__name__)

    def __init__(self):
        mysql = MySql(mysql_config)
        self.db = mysql.get_session()
        self.plaid_config = plaid_config
        self._init_facets()

    def _init_facets(self):
        self.create_security = create_security
        self.create_holding = create_holding
        self.create_investment_transaction = create_investment_transaction
        self.get_security_by_security_id = get_security_by_security_id
        self.get_security_by_symbol = get_security_by_symbol
        self.get_securities_by_account = get_securities_by_account
        self.get_securities = get_securities
        self.get_holdings_by_profile_and_account = get_holdings_by_profile_and_account
        self.get_holding_by_plaid_account_id_and_plaid_security_id =\
            get_holding_by_plaid_account_id_and_plaid_security_id
        self.update_holding_balance = update_holding_balance
        self.update_holding_balance = update_holding_balance

    def sync_holdings(self, profile: Profile, account: Account):
        if profile is None:
            self.logger.error("requested holdings sync on account with no Profile given")
            return

        if account is None:
            self.logger.error("requested holdings sync on account with no Account given")
            return

        plaid_item = get_plaid_item_by_id(self, account.plaid_item_id)
        if plaid_item is None:
            self.logger.error("requested holdings sync on account but couldn't find plaid_item: {0}"
                              .format(account.to_dict()))
            return

        api = Investments(InvestmentsConfig(self.plaid_config))
        investment_dict = api.get_investments(plaid_item.access_token)

        # update securities from this account
        # these might not be account specific, but institution specific
        # so there's a chance I can detach it from the profile/account and just
        # link it in from the holdings
        for security_dict in investment_dict["securities"]:
            security = self.get_security_by_security_id(plaid_security_id=security_dict['security_id'])
            if security is None:
                security = self.create_security(CreateSecurityRequest(
                    profile=profile,
                    account=account,
                    name=security_dict['name'],
                    ticker_symbol=security_dict['ticker_symbol'],
                    iso_currency_code=security_dict['iso_currency_code'],
                    institution_id=security_dict['institution_id'],
                    institution_security_id=security_dict['institution_security_id'],
                    security_id=security_dict['security_id'],
                    proxy_security_id=security_dict['proxy_security_id'],
                    cusip=security_dict['cusip'],
                    isin=security_dict['isin'],
                    sedol=security_dict['sedol']
                ))

        # update the holdings
        for holding_dict in investment_dict["holdings"]:
            security = self.get_security_by_security_id(holding_dict['security_id'])
            holding = self.get_holding_by_plaid_account_id_and_plaid_security_id(
                holding_dict["account_id"],
                holding_dict["security_id"])
            if holding is None:
                holding = self.create_holding(CreateHoldingRequest(
                    account=account,
                    security=security,
                    cost_basis=holding_dict['cost_basis'],
                    quantity=holding_dict['quantity'],
                    iso_currency_code=holding_dict['iso_currency_code']
                ))
            else:
                self.update_holding_balance(UpdateHoldingRequest(
                    holding=holding,
                    cost_basis=holding_dict['cost_basis'],
                    quantity=holding_dict['quantity']
                ))

    def sync_transactions(self, profile: Profile, account: Account):
        if account is None:
            self.logger.error("requested holdings sync on account that couldn't be found: {0}".format(account_id))
            return

        plaid_item = self.db.query(PlaidItem).where(PlaidItem.id == account.plaid_item_id).first()
        if plaid_item is None:
            self.logger.error(
                "requested holdings sync on account but couldn't find plaid_item: {0}".format(account.to_dict()))
            return

        api = Investments(InvestmentsConfig(self.plaid_config))

        # if we have no transactions for this account, try and pull the last years
        # otherwise, we probably got a notification from a webhook to update, so just
        # update the last week's worth of transactions
        start = date.today()
        end = start - timedelta(days=365)

        if self._has_transactions(account):
            end = start - timedelta(days=7)

        transactions_dict = api.get_transactions(plaid_item.access_token, start=start, end=end)

        if 'transactions' not in transactions_dict:
            self.logger.info("upstream provider returned 0 transactions for date period {0} - {1}"
                             .format(start, end))
            return

        transactions = []

        for transaction_dict in transactions_dict:
            if 'account_id' not in transaction_dict:
                self.logger.error("upstream gave investment transaction result with missing account id: {0}",
                                  transaction_dict)
                continue

            investment_transaction = self._get_investment_transaction_by_investment_transaction_id(
                transaction_dict['investment_transaction_id'])

            if investment_transaction is None:
                investment_transaction = self.create_investment_transaction(CreateInvestmentTransactionRequest(
                    account=account,
                    amount=transaction_dict['amount'],
                    date=transaction_dict['date'],
                    fees=transaction_dict['fees'],
                    investment_transaction_id=transaction_dict['investment_transaction_id'],
                    iso_currency_code=transaction_dict['iso_currency_code'],
                    name=transaction_dict['name'],
                    price=transaction_dict['price'],
                    quantity=transaction_dict['quantity'],
                    subtype=transaction_dict['subtype'],
                    type=transaction_dict['type']
                ))

            transactions.append(transactions)

        return transactions

    def _has_transactions(self, account: Account) -> bool:
        r = self.db.query(InvestmentTransaction).filter(InvestmentTransaction.account_id == account.id).count() > 0
        return r

    def _get_investment_transaction_by_investment_transaction_id(self, investment_transaction_id):
        return self.db.query(InvestmentTransaction).filter(InvestmentTransaction.investment_transaction_id ==
                                                           investment_transaction_id).first()
