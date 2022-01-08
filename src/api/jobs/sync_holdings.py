from core.repositories import HoldingRepository, PlaidRepository
from core.stores.database import Database
from core.lib.logger import get_logger
from api.metrics.job_metrics import PERF_JOB_SYNC_HOLDINGS

from config import config

class SyncHoldings:

    plaid_item_id = None
    db = Database(config.api)

    def __init__(self, redis_message=None):
        self.logger = get_logger(__name__)
        if redis_message is None or 'plaid_item_id' not in redis_message['args']:
            self.logger.error("attempting to run holding sync job without a valid PlaidItem id: {0}"
                              .format(redis_message))
        self.plaid_repo = PlaidRepository(self.db)
        self.holding_repo = HoldingRepository(self.db)
        self.plaid_item_id = redis_message['args']['plaid_item_id']

    @PERF_JOB_SYNC_HOLDINGS.time()
    def run(self):
        if self.plaid_item_id:
            self.logger.info(
                "updating holdings for plaid item id: {0}".format(self.plaid_item_id))
            plaid_item = self.plaid_repo.get_plaid_item_by_id(
                self.plaid_item_id)
            self.holding_repo.update_holdings(plaid_item)
        else:
            self.logger.error(
                "not running holding sync, no PlaidItem id found: {0}".format(self.plaid_item_id))
