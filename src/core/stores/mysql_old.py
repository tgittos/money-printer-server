import sys
sys.path.append('./../../src')

import pandas
from datetime import datetime, timedelta
from sqlalchemy import and_, cast, Time

from lib.finnhub.data import FinnhubData
from models.candle import Candle
from models.sync import Sync
from lib.db import Db

class MysqlOld:
    
    def __init__(self, echo=False):
        db = Db(echo=echo)
        self.fh = FinnhubData()
        self.db = db.get_session()
    
    def add_to_sync(self, symbol, resolution):
        s = self.get_sync(symbol)
        if s != None:
            s = Sync(symbol=symbol)
            self.db.add(s)
            self.db.commit()
        return s
    
    def remove_from_sync(self, symbol):
        s = self.db.query(Sync).filter(Sync.symbol == symbol).all()
        self.db.delete(s)
        self.db.commit()
        return None
    
    def get_sync(self, symbol = None):
        if symbol == None:
            db_data = list(self.db.query(Sync).all())
        else:
            db_data = self.db.query(Sync).filter(Sync.symbol == symbol).all()
        return db_data
    
    def _update_sync(self, symbol):
        s = self.db.query(Sync).filter(Sync.symbol == symbol).all()
        if len(s) == 0:
            s = Sync(symbol=symbol)
            self.db.add(s)
        else:
            s = s[0]
        s.last_update = datetime.now()
        self.db.commit()
        return None
    
    def update_candles(self, symbol, resolution, debug=False):
        s = self.get_sync(symbol)
        if len(s) > 0 and s[0].last_update != None:
            days = (datetime.today() - s[0].last_update).days
            self.fh.get_historical_data(symbol, self._incremental_save_candles_df, days=days, debug=debug)
        else:
            self.fh.get_historical_data(symbol, self._incremental_save_candles_df, debug=debug)
            self.add_to_sync(symbol, resolution)
        self._update_sync(symbol)
        return self.get_candles_by_symbol(symbol, resolution)
    
    def get_candles_by_symbol(self, symbol, resolution=FinnhubData.sixty_min):
        db_data = list(self.db.query(Candle).filter(Candle.symbol == symbol))
        return self._convert_to_dataframe(db_data)
    
    def get_candles_by_symbol_in_window(self, symbol, start, end, resolution=FinnhubData.sixty_min, debug=False):
        return self._get_candles_by_time_window(symbol, start, end, resolution, debug=debug)
    
    def get_closes_by_symbol(self, symbol):
        db_data = list(self.db.query(Candle).filter(and_(Candle.symbol == symbol,
            cast(Candle.timestamp, Time) == '21:00:00')))
        if len(db_data) == 0:
            return pandas.DataFrame()
        return self._convert_to_dataframe(db_data)
    
    def _incremental_save_candles_df(self, symbol, current_date, resolution, debug=False):
        if debug:
            print("checking db for {0} {1} candles for {2}".format(symbol, resolution, current_date))
        if not self._symbol_day_exists(symbol, resolution, current_date):
            if debug:
                print("db miss, fetching from finnhub")
            df = self.fh.stock_candles_by_date(symbol, current_date, debug=debug)
            if not df.empty:
                if debug:
                    print("saving candle: {0}".format(df))
                return self._save_candles_df(symbol, current_date, resolution, df)
    
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
                                  close=c['c'], high=c['h'], low=c['l'], volume=c['v'])
                new_rows = new_rows + [new_candle]
                rows = rows + [new_candle]
            else:
                new_candle = Candle(symbol=symbol, resolution=resolution, timestamp=existing['t'],
                    open=existing['o'], close=existing['c'], high=existing['h'],
                    low=existing['l'], volume=existing['v'])
                rows = rows + [new_candle]
                
        self.db.add_all(new_rows)
        self.db.commit()
        return self._convert_to_dataframe(rows)
    
    def _get_candles_by_day(self, symbol, resolution, day, debug=False):
        start_of_day = day.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        return self._get_candles_by_time_window(symbol, start_of_day, end_of_day, resolution, debug=debug)
    
    def _symbol_day_exists(self, symbol, resolution, day):
        start_of_day = day.replace(hour=0, minute=0, second=0, microsecond=0)
        end_of_day = start_of_day + timedelta(days=1)
        db_data = self.db.query(Candle).filter(and_(Candle.symbol == symbol,
            Candle.timestamp >= start_of_day,
            Candle.timestamp <= end_of_day)).count()
        return db_data > 0
    
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