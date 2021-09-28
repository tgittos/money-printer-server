from core.repositories.plaid_repository import PlaidRepository
from core.repositories.balance_repository import BalanceRepository
from core.lib.logger import get_logger

class SyncBalances:

    plaid_item_id = None

    def __init__(self, redis_message=None):
        self.logger = get_logger(__name__)
        if redis_message is None or 'plaid_item_id' not in redis_message['args']:
            self.logger.error("attempting to run balance sync job without a valid PlaidItem id: {0}"
                              .format(redis_message))
        self.plaid_repo = PlaidRepository()
        self.balance_repo = BalanceRepository()
        self.plaid_item_id = redis_message['args']['plaid_item_id']

    def run(self):
        if self.plaid_item_id:
            self.logger.info("syncing balances for plaid_item_id {0}".format(self.plaid_item_id))
            plaid_item = self.plaid_repo.get_plaid_item_by_id(self.plaid_item_id)
            self.balance_repo.sync_all_balances(plaid_item)
            self.logger.info("done syncing balances")
        else:
            self.logger.error("not running balance sync, no PlaidItem id found: {0}".format(self.plaid_item_id))
