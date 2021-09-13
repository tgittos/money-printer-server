from datetime import datetime

from core.apis.plaid.common import PlaidApiConfig
from core.apis.plaid.accounts import Accounts, AccountsConfig
from core.repositories.profile_repository import get_repository as get_profile_repository
from core.repositories.plaid_repository import get_repository as get_plaid_repository, GetPlaidItem
from core.repositories.account_repository import get_repository as get_account_repository, CreateAccountRequest
from core.repositories.balance_repository import get_repository as get_balance_repository, CreateBalanceRequest
from core.models.account import Account

from server.services.api import load_config

app_config = load_config()

sql_config = app_config['db']

plaid_config = PlaidApiConfig()
plaid_config.env = app_config['plaid']['env']
plaid_config.client_id = app_config['plaid']['client_id']
plaid_config.secret = app_config['plaid']['secret']


class SyncAccounts:

    def __init__(self, redis_message):
        self.profile_id = redis_message['profile_id']
        self.plaid_link_id = redis_message['plaid_item_id']
        self.plaid_repo = get_plaid_repository(sql_config=sql_config, plaid_api_config=plaid_config)

    def run(self):
        profile = self.__fetch_profile()
        plaid_link = self.__fetch_plaid_link()
        if profile is None or plaid_link is None:
            print(" * error syncing accounts - either profile or plaid link is None! profile: {0}, plaid_link: {1}".format(
                profile,
                plaid_link
            ), flush=True)
            return

        plaid_accounts_api = Accounts(AccountsConfig(
            plaid_config=plaid_config
        ))
        print(" * fetching auths from Plaid using access token: {0}".format(plaid_link.access_token), flush=True)
        plaid_accounts_dict = plaid_accounts_api.get_accounts(plaid_link.access_token)

        print(" * updating {0} accounts".format(len(plaid_accounts_dict['accounts'])), flush=True)
        account_repo = get_account_repository()
        balance_repo = get_balance_repository(mysql_config=sql_config)
        for account_dict in plaid_accounts_dict['accounts']:
            account = account_repo.get_account_by_account_id(account_dict['account_id'])
            if account is None:
                account = account_repo.create_account(CreateAccountRequest(
                    account_id=account_dict['account_id'],
                    name=account_dict['name'],
                    official_name=account_dict['official_name'],
                    subtype=account_dict['subtype'],
                    plaid_item_id=plaid_link.id,
                    profile_id=profile.id
                ))

            print(" * updating balance for account {0}", account.account_id, flush=True)
            balance_dict = account_dict['balances']
            latest_balance = balance_repo.create_balance(CreateBalanceRequest(
                account_id=account.id,
                available=balance_dict['available'],
                current=balance_dict['current'],
                iso_currency_code=balance_dict['iso_currency_code']
            ))

    def __fetch_profile(self):
        repo = get_profile_repository()
        return repo.get_by_id(self.profile_id)

    def __fetch_plaid_link(self):
        return self.plaid_repo.get_plaid_item(GetPlaidItem(
            id=self.plaid_link_id
        ))
