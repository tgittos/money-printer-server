import sys
sys.path.append('./../../src')

import pandas
from datetime import timedelta
from sqlalchemy import and_, cast, Time

from lib.finnhub.data import FinnhubData
from models.candle import Candle
from db import Db

class Mysql:
    
    def __init__(self, echo=False):
        db = Db(echo=echo)
        self.fh = FinnhubData()
        self.db = db.get_session()
    
    def update_candles(self, symbol, resolution, debug=False):
        historical_candles = self.fh.get_historical_data(symbol, self._incremental_save_candles_df, debug=debug)
        return historical_candles
    
    def get_candles_by_symbol(self, symbol, resolution=FinnhubData.thirty_min):
        db_data = list(self.db.query(Candle).filter(and_(Candle.symbol == symbol,
            Candle.resolution == resolution)))
        if len(db_data) == 0:
            return pandas.DataFrame()
        return self._convert_to_dataframe(db_data)
    
    def get_closes_by_symbol(self, symbol):
        db_data = list(self.db.query(Candle).filter(and_(Candle.symbol == symbol,
            cast(Candle.timestamp, Time) == '21:00:00')))
        if len(db_data) == 0:
            return pandas.DataFrame()
        return self._convert_to_dataframe(db_data)
    
    def _incremental_save_candles_df(self, symbol, current_date, resolution, debug=False):
        if debug:
            print("checking db for {0} {1} candles for {2}".format(symbol, resolution, current_date))
        df = self._get_candles_by_day(symbol, resolution, current_date, debug=debug)
        if df.empty:
            if debug:
                print("db miss, fetching from finnhub")
            df = self.fh.stock_candles_by_date(symbol, current_date, debug=debug)
            if df.empty:
                return df
            if debug:
                print("saving candle: {0}".format(df))
            return self._save_candles_df(symbol, current_date, resolution, df)
        else:
            if debug:
                print("found candle: {0}".format(df))
            return df
    
    def _save_candles_df(self, symbol, current_date, resolution, candles):
        new_rows = []
        rows = []
        # look for existing candle at given resolution
        existing = self._get_candles_by_day(symbol, resolution, current_date)
        for i in range(0, len(candles)):
            if i == 0:
                next
            c = candles.iloc[i]
            if not c['t'] in existing:
                new_candle = Candle(symbol=symbol, resolution=resolution, timestamp=c['t'], open=c['o'],
                                  close=c['c'], high=c['h'], low=c['l'], returns=c['r'], volume=c['v'])
                new_rows = new_rows + [new_candle]
                rows = rows + [new_candle]
            else:
                new_candle = Candle(symbol=symbol, resolution=resolution, timestamp=existing['t'],
                    open=existing['o'], close=existing['c'], high=existing['h'],
                    low=existing['l'], returns=existing['r'], volume=existing['v'])
                rows = rows + [new_candle]
                
        self.db.add_all(new_rows)
        self.db.commit()
        return self._convert_to_dataframe(rows)
    
    def _get_candles_by_day(self, symbol, resolution, day, debug=False):
        start_of_day = day.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        return self._get_candles_by_time_window(symbol, start_of_day, end_of_day, resolution, debug=debug)
    
    def _get_candle_by_timestamp(self, symbol, resolution, timestamp):
        db_data = list(self.db.query(Candle).filter(and_(Candle.symbol == symbol,
            Candle.timestamp == timestamp)))
        if len(db_data) == 0:
            return pandas.DataFrame()
        return self._convert_to_dataframe(db_data)
        
    def _get_candles_by_time_window(self, symbol, start, end, resolution = FinnhubData.sixty_min, debug=False):
        if debug:
            print("checking for {0} {1} candles for {2} - {3}".format(symbol, resolution, start, end))
        db_data = list(self.db.query(Candle).filter(and_(Candle.symbol == symbol,
            Candle.timestamp >= start,
            Candle.timestamp <= end)))
        return self._convert_to_dataframe(db_data)
    
    def _convert_to_dataframe(self, candles):
        candle_rows = []
        for c in candles:
            candle_rows = candle_rows + [c.as_dict()]
        return pandas.DataFrame.from_records(candle_rows)