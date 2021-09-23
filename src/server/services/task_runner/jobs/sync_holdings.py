from datetime import datetime

from core.apis.plaid.common import PlaidApiConfig
from core.apis.mailgun import MailGunConfig
from core.repositories.holding_repository import get_repository as get_holdings_repository
from core.lib.logger import get_logger

from server.services.api import load_config
from server.config import config as server_config
app_config = load_config()

mysql_config = app_config['db']
iex_config = app_config['iexcloud']

plaid_config = PlaidApiConfig()
plaid_config.env = app_config['plaid']['env']
plaid_config.client_id = app_config['plaid']['client_id']
plaid_config.secret = app_config['plaid']['secret']

mailgun_config = MailGunConfig(
    server_config['mailgun']['api_key'],
    server_config['mailgun']['domain']
)


class SyncHoldings:

    plaid_item_id = None

    def __init__(self, redis_message=None):
        self.logger = get_logger(__name__)
        if redis_message is not None and 'plaid_item_id' in redis_message['args']:
            self.plaid_item_id = redis_message['args']['plaid_item_id']
        self.holding_repo = get_holdings_repository(mysql_config=mysql_config, iex_config=iex_config,
                                                    plaid_config=plaid_config, mailgun_config=mailgun_config)

    def run(self):
        if self.plaid_item_id:
            self.logger.info("updating holdings for plaid item id: {0}".format(self.plaid_item_id))
            self.holding_repo.update_holdings(self.plaid_item_id)
