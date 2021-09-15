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

    profile_id = None
    plaid_item_id = None

    def __init__(self, redis_message=None):
        if redis_message is not None and 'profile_id' in redis_message and 'plaid_item_id' in redis_message:
            self.profile_id = redis_message['profile_id']
            self.plaid_item_id = redis_message['plaid_item_id']
        self.plaid_repo = get_plaid_repository(sql_config=sql_config, plaid_api_config=plaid_config)

    def run(self):
        if self.profile_id and self.plaid_item_id:
            self.sync_profile(self.profile_id, self.plaid_item_id)
            return
        self.sync_all_profiles()

    def sync_all_profiles(self):
        print(" * syncing all profiles", flush=True)
        profile_repo = get_profile_repository()
        plaid_repo = get_plaid_repository(sql_config=sql_config, plaid_api_config=plaid_config)
        all_profiles = profile_repo.get_all_profiles()
        for profile in all_profiles:
            plaid_links = plaid_repo.get_plaid_items_by_profile(profile.id)
            for plaid_link in plaid_links:
                self.sync_profile(profile.id, plaid_link.id)

    def sync_profile(self, profile_id, plaid_link_id):
        profile_repo = get_profile_repository()
        profile = profile_repo.get_by_id(profile_id)

        if profile is None:
            print(" * error syncing accounts - could not find requested profile {0}".format(profile_id), flush=True)
            return

        account_repo = get_account_repository()
        account_repo.sync_all_accounts(profile_id)
