import redis
import json

from core.repositories.stock_repository import get_repository as get_stock_repository
from core.lib.logger import get_logger
from config import mysql_config, iex_config, redis_config


class HistoricalClient:

    running = False
    thread = None

    def __init__(self):
        self.logger = get_logger(__name__)
        self.r = redis.Redis(host=redis_config.host, port=redis_config.port, db=0)
        self.p = self.r.pubsub()
        self.repository = get_stock_repository(iex_config=iex_config, mysql_config=mysql_config)

    def start(self):
        self.running = True
        self.thread = self.p.run_in_thread(sleep_time=0.1)
        self.p.subscribe(**{'historical_quotes': self.__handle_message})

    def stop(self):
        self.running = False
        self.p.unsubscribe('historical_quotes')
        if self.thread:
            self.thread.join()

    def get_historical_daily(self, symbol, start=None, end=None):
        self.logger.debug("get_historical_daily request for symbol {0}, {1} - {2}".format(
            symbol, start, end
        ))
        data = self.repository.historical_daily(symbol, start=start, end=end)
        return json.dumps(data)

    def get_historical_intraday(self, symbol, start=None):
        self.logger.debug("get_historical_intraday request for symbol {0}, {1}".format(
            symbol, start
        ))
        data = self.repository.historical_intraday(symbol, start=start)
        return json.dumps(data)

    def __handle_message(self, data):
        json_data = json.loads(data['data'])

        symbol = json_data['symbol']
        type = json_data['type']
        start = json_data['start']
        end = json_data['end']

        if type == 'daily':
            data = self.get_historical_daily(symbol, start, end)

        if type == 'intraday':
            data = self.get_historical_intraday(symbol, start)

        if data is not None:
            self.__dispatch({
                'symbol': symbol,
                'type': type,
                'start': start,
                'end': end,
                'data': json.dumps(data)
            })

    def __dispatch(self, dict_message):
        if self.r is not None:
            self.r.publish('historical_quotes', json.dumps(dict_message))
