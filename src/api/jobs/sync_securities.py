from core.repositories.stock_repository import StockRepository
from core.repositories.security_repository import SecurityRepository
from core.lib.logger import get_logger


class SyncSecurities:

    symbol = None

    def __init__(self, redis_message=None):
        self.logger = get_logger(__name__)
        if redis_message is not None and 'symbol' in redis_message['args']:
            self.symbol = redis_message['args']['symbol']
        self.stock_repo = StockRepository()
        self.security_repo = SecurityRepository()

    def run(self):
        if self.symbol is not None:
            security = self.security_repo.get_security_by_symbol(self.symbol)
            self.sync_security(security)
        else:
            self.sync_all_securities()
        self.logger.info("done running sync_securities")

    def sync_all_securities(self):
        self.logger.info("syncing all tracked securities")
        securities = self.security_repo.get_securities()
        if len(securities) == 0:
            self.logger.info("no securities tracked, shutting down")
        for security in securities:
            self.sync_security(security)

    def sync_security(self, security):
        self.logger.info("syncing security with ticker {0}".format(security.ticker_symbol))
        has_data = self.stock_repo.has_data(security.ticker_symbol)
        if not has_data:
            self.logger.info("no historical data found for security, fetching default window of back data")
            # fetch the default window's worth of historical daily closings
            self.stock_repo.historical_daily(security.ticker_symbol)
        else:
            self.logger.info("updating prices with last EOD")
            # just fetch the last EOD prices
            self.__sync_eod_symbol(security.id, security.ticker_symbol)

    def __sync_eod_symbol(self, security_id, symbol):
        # the repo method will automatically persist the data for us
        self.stock_repo.previous(symbol)

