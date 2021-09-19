
from core.repositories.stock_repository import get_repository as get_stock_repository

from server.config import config as server_config
from core.stores.mysql import MySql


def get_repository(mysql_config, iex_config):
    repo = HoldingRepository(HoldingRepositoryConfig(
        mysql_config=mysql_config,
        iex_config=iex_config
    ))
    return repo


class HoldingRepositoryConfig:
    def __init__(self, mysql_config, iex_config):
        self.mysql_config = mysql_config
        self.iex_config = iex_config


class HoldingRepository:

    def __init__(self, config):
        self.mysql_config = config.mysql_config
        self.iex_config = config.iex_config
        db = MySql(self.mysql_config)
        self.db = db.get_session()
        self.stock_repo = get_stock_repository(iex_config=self.iex_config, mysql_config=self.mysql_config)

    def calculate_performance(self, holding_id):
        # pull the holding
        # pull security_prices for holding
        # using cost basis of holding, at each security_price data point, calculate a rate of return
        raise Exception("Not implemented")

    def calculate_forecast(self, holding_id):
        raise Exception("Not implemented")

