from datetime import datetime

from core.apis.plaid.common import PlaidApiConfig
from core.apis.mailgun import MailGunConfig
from core.repositories.profile_repository import get_repository as get_profile_repository
from core.repositories.account_repository import get_repository as get_account_repository, CreateAccountRequest

from server.services.api import load_config
from server.config import config as server_config
app_config = load_config()

sql_config = app_config['db']

plaid_config = PlaidApiConfig()
plaid_config.env = app_config['plaid']['env']
plaid_config.client_id = app_config['plaid']['client_id']
plaid_config.secret = app_config['plaid']['secret']

mailgun_config = MailGunConfig(
    server_config['mailgun']['api_key'],
    server_config['mailgun']['domain']
)


class SyncAccounts:

    profile_id = None
    plaid_item_id = None

    def __init__(self, redis_message=None):
        if redis_message is not None and 'profile_id' in redis_message and 'plaid_item_id' in redis_message:
            self.profile_id = redis_message['profile_id']
            self.plaid_item_id = redis_message['plaid_item_id']
        self.profile_repo = get_profile_repository(mysql_config=sql_config, mailgun_config=mailgun_config)
        self.account_repo = get_account_repository(mysql_config=sql_config, plaid_config=plaid_config)

    def run(self):
        if self.profile_id and self.plaid_item_id:
            self.sync_profile(self.profile_id, self.plaid_item_id)
            return
        self.sync_all_profiles()

    def sync_all_profiles(self):
        print(" * syncing all profiles", flush=True)
        all_profiles = self.profile_repo.get_all_profiles()
        for profile in all_profiles:
            self.sync_profile(profile.id)

    def sync_profile(self, profile_id):
        profile = self.profile_repo.get_by_id(profile_id)

        if profile is None:
            print(" * error syncing accounts - could not find requested profile {0}".format(profile_id), flush=True)
            return

        self.account_repo.sync_all_accounts(profile_id)
