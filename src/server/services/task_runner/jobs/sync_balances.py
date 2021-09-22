from datetime import datetime

from core.apis.plaid.common import PlaidApiConfig
from core.apis.mailgun import MailGunConfig
from core.repositories.profile_repository import get_repository as get_profile_repository
from core.repositories.balance_repository import get_repository as get_balance_repository
from core.lib.logger import get_logger

from server.services.api import load_config
from server.config import config as server_config
app_config = load_config()

mysql_config = app_config['db']

plaid_config = PlaidApiConfig()
plaid_config.env = app_config['plaid']['env']
plaid_config.client_id = app_config['plaid']['client_id']
plaid_config.secret = app_config['plaid']['secret']

mailgun_config = MailGunConfig(
    server_config['mailgun']['api_key'],
    server_config['mailgun']['domain']
)


class SyncAccounts:

    plaid_item_id = None

    def __init__(self, redis_message=None):
        self.logger = get_logger(__name__)
        if redis_message is not None and 'plaid_item_id' in redis_message:
            self.plaid_item_id = redis_message.args['plaid_item_id']

        self.profile_repo = get_profile_repository(mysql_config=mysql_config, mailgun_config=mailgun_config)
        self.balance_repo = get_balance_repository(mysql_config=mysql_config, plaid_config=plaid_config)

    def run(self):
        if self.plaid_item_id:
            self.logger.info("syncing balances for plaid_item_id {0}", self.plaid_item_id)
            self.balance_repo.sync_all_balances(self.plaid_item_id)
