from core.repositories.plaid_repository import PlaidRepository
from core.repositories.profile_repository import ProfileRepository
from core.stores.mysql import MySql
from config import mysql_config
from core.lib.logger import get_logger


class SyncAccounts:

    plaid_item_id = None

    def __init__(self, redis_message):
        self.logger = get_logger(__name__)
        if redis_message is None or 'plaid_item_id' not in redis_message['args']:
            self.logger.error("attempting to run account sync job without a valid PlaidItem id: {0}"
                              .format(redis_message))
        self.store = MySql(mysql_config)
        self.plaid_repo = PlaidRepository(self.store)
        self.profile_repo = ProfileRepository(self.store)
        self.plaid_item_id = redis_message['args']['plaid_item_id']

    def run(self):
        if self.plaid_item_id:
            plaid_item = self.plaid_repo.get_plaid_item_by_id(self.plaid_item_id)
            if not plaid_item:
                self.logger.error("not running account sync, couldnt find PlaidItem with id: {0}"
                                  .format(self.plaid_item_id))
                return
            self.profile_repo.sync_all_accounts(plaid_item)
        else:
            self.logger.error("not running account sync, no PlaidItem id found: {0}".format(self.plaid_item_id))
