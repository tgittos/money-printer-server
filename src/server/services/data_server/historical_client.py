import redis
import json

from core.repositories.stock_repository import get_repository as get_stock_repository

from server.services.api import load_config
app_config = load_config()

mysql_config = app_config['db']
iex_config = app_config['iexcloud']


class HistoricalClient:

    def __init__(self):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.p = self.r.pubsub()
        self.p.subscribe(**{'historical_quotes': self.__handle_message})
        self.thread = self.p.run_in_thread(sleep_time=0.1)
        self.repository = get_stock_repository(iex_config=iex_config, mysql_config=mysql_config)

    def get_historical_daily(self, symbol, start=None, end=None):
        data = self.repository.historical_daily(symbol, start=start, end=end)
        return json.dumps(data)

    def get_historical_intraday(self, symbol, start=None):
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
