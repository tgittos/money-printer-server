import sys
sys.path.append('./../../src')

from os import path
from datetime import date, datetime, timedelta
import time
import calendar

import finnhub
import pandas

import config
from lib.stonk_jar import StonkJar

class FinnhubData:

    # Time periods
    one_min = '1'
    five_min = '5'
    fifteen_min = '15'
    thirty_min = '30'
    sixty_min = '60'
    day = 'D'
    week = 'W'
    month = 'M'

    # Market settings (defaulted to CST)
    local_market_open_hour = 8
    local_market_open_min = 30

    local_market_close_hour = 15
    local_market_close_min = 0

    def __init__(self):
        self.finnhub_client = finnhub.Client(api_key=config.api_keys['finnhub']['live'])
        self.jar = None
        self.sleep_for = 3

    def init_jar(self, ticker):
        self.jar = StonkJar(ticker)

    def recommendation_trends_by_date(self, ticker, date, include_ah = True, pickle = True, debug = False):
        first_of_month = date.replace(day = 1)
        pickle_name = "{0}.recommendations.{1}.pkl".format(ticker, first_of_month.strftime('%Y-%m-%d'))
        
        if pickle and self.jar == None:
            self.init_jar(ticker)
            
        if pickle:
            recommendations = self.jar.pickle_back(
                pickle_name,
                self._api_call_with_sleep,
                self.finnhub_client.recommendation_trends, ticker)
        else:
            recommendations = self.api_call_with_sleep(self.finnhub_client.recommendation_trends, ticker)
            
        recommendation = [r for r in recommendations if datetime.strptime(r['period'], '%Y-%m-%d').date() == first_of_month]
        if (len(recommendation) > 0):
            return recommendation[0]
        return {}

    def company_earnings_by_date(self, ticker, date, include_ah = True, pickle = True, debug = False):
        reporting_period = timedelta(days = 90)
        pickle_name = "{0}.earnings.{1}.pkl".format(ticker, date.strftime('%Y-%m-%d'))
        
        if pickle and self.jar == None:
            self.init_jar(ticker)
        
        if pickle:
            earnings = self.jar.pickle_back(
                pickle_name,
                self._api_call_with_sleep,
                self.finnhub_client.company_earnings, ticker)
        else:
            earnings = self.finnhub_client.company_earnings(ticker)
            
        earning = [r for r in earnings if datetime.strptime(r['period'], '%Y-%m-%d').date() + reporting_period > date]
        if (len(earning) > 0):
            return earning[0]
        return {}

    def get_candle_as_dataframe(self, ticker, time_period, start_ts, end_ts, pickle = True, debug = False):
        candles = None

        if debug:
            print("[get_candle_as_dataframe] fetching {0} data for {1} - {2}".format(
            time_period, datetime.fromtimestamp(start_ts), datetime.fromtimestamp(end_ts)))
            
        pickle_name = "{0}.{1}.candles.{2}.{3}.pkl".format(ticker, time_period, start_ts, end_ts)

        if pickle:
            if self.jar == None:
                self.init_jar(ticker)
            candles = self.jar.pickle_back(
                pickle_name,
                self._api_call_with_sleep,
                self.finnhub_client.stock_candles, ticker, time_period, start_ts, end_ts)
            if debug:
                print("[get_candle_as_dataframe] data from pickle: {0}".format(candles))
        else:
            candles = self._api_call_with_sleep(self.finnhub_client.stock_candles, ticker, time_period, start_ts, end_ts)
            if debug:
                print("[get_candle_as_dataframe] data from finnhub: {0}".format(candles))

        if 's' in candles and candles['s'] == 'no_data':
            return pandas.DataFrame()

        candle_rows = list(zip(candles['t'], candles['l'], candles['o'], candles['c'], candles['h'], candles['v']))    
        df = pandas.DataFrame.from_records(candle_rows)
        df[0] = pandas.to_datetime(df[0], unit = 's')
        df.sort_index
        
        return df

    def get_daily_closings(self, ticker, date = datetime.today(), include_ah = False, pickle = True, debug = False):
        pre_candles = []
        post_candles = []
        start_ts = int(date.replace(hour=FinnhubData.local_market_open_hour, minute=FinnhubData.local_market_open_min, second=1).timestamp())
        end_ts = int(date.replace(hour=FinnhubData.local_market_close_hour, minute=FinnhubData.local_market_close_min, second=1).timestamp())

        if include_ah:
            pre_start_ts = int(date.replace(hour=FinnhubData.local_market_open_hour-4, minute=FinnhubData.local_market_open_min-30, second=1).timestamp())
            post_close_ts = int(date.replace(hour=FinnhubData.local_market_close_hour+4, minute=FinnhubData.local_market_close_min, second=1).timestamp())

            if debug:
                print("[get_daily_closings] fetching pre market candles")
            pre_candles_df = self.get_candle_as_dataframe(ticker, 60, pre_start_ts, start_ts, pickle = pickle, debug = debug)
            pre_candles = pre_candles_df.tail(1).values.tolist()
            if debug:
                print("[get_daily_closings] pre_candles: {0}".format(pre_candles))

            if debug:
                print("[get_daily_closings] fetching post market candles")
            post_candles_df = self.get_candle_as_dataframe(ticker, 60, end_ts, post_close_ts, pickle = pickle, debug = debug)
            post_candles = post_candles_df.tail(1).values.tolist()
            if debug:
                print("[get_daily_closings] post_candles: {0}".format(post_candles))

        if debug:
            print("[get_daily_closings] fetching market end candles")
        candles_df = self.get_candle_as_dataframe(ticker, 60, start_ts, end_ts, pickle = pickle, debug = debug)
        candles = candles_df.tail(1).values.tolist()
        if debug:
            print("[get_daily_closings] candles: {0}".format(candles))

        retVal = []
        if len(pre_candles) > 0:
            retVal = retVal + pre_candles
        retVal = retVal + candles
        if len(post_candles) > 0:
            retVal = retVal + post_candles

        if debug:
            print("[get_daily_closings] retVal: {0}".format(retVal))

        df = pandas.DataFrame.from_records(retVal)

        if len(df.columns):
            df.columns = ['t', 'o', 'l', 'h', 'c', 'v']
            df['t'] = pandas.to_datetime(df['t'], unit = 's')
            df.sort_index

        if debug and len(df.columns):
            print(df.describe())

        return df

    def stock_candles_by_date(self, ticker, date, time_period = 60, include_ah = True, pickle = True, debug = False):
        pre_candles = []
        post_candles = []
        start_ts = int(date.replace(hour=FinnhubData.local_market_open_hour, minute=FinnhubData.local_market_open_min, second=1).timestamp())
        end_ts = int(date.replace(hour=FinnhubData.local_market_close_hour, minute=FinnhubData.local_market_close_min, second=1).timestamp())

        if include_ah:
            pre_start_ts = int(date.replace(hour=FinnhubData.local_market_open_hour-4, minute=FinnhubData.local_market_open_min-30, second=1).timestamp())
            post_close_ts = int(date.replace(hour=FinnhubData.local_market_close_hour+4, minute=FinnhubData.local_market_close_min, second=1).timestamp())

            if debug:
                print("[stock_candles_by_date] fetching pre market candles")
            pre_candles_df = self.get_candle_as_dataframe(ticker, time_period, pre_start_ts, start_ts, pickle = pickle, debug = debug)
            pre_candles = pre_candles_df[:].values.tolist()
            if debug:
                print("[stock_candles_by_date] pre_candles: {0}".format(pre_candles))

            if debug:
                print("[stock_candles_by_date] fetching post market candles")
            post_candles_df = self.get_candle_as_dataframe(ticker, time_period, end_ts, post_close_ts, pickle = pickle, debug = debug)
            post_candles = post_candles_df[:].values.tolist()
            if debug:
                print("[stock_candles_by_date] post_candles: {0}".format(post_candles))

        if debug:
            print("[stock_candles_by_date] fetching market end candles")
        candles_df = self.get_candle_as_dataframe(ticker, time_period, start_ts, end_ts, pickle = pickle, debug = debug)
        candles = candles_df[:].values.tolist()
        if debug:
            print("[stock_candles_by_date] candles: {0}".format(candles))

        retVal = []
        if len(pre_candles) > 0:
            retVal = retVal + pre_candles
        retVal = retVal + candles
        if len(post_candles) > 0:
            retVal = retVal + post_candles

        if debug:
            print("[stock_candles_by_date] retVal: {0}".format(retVal))

        df = pandas.DataFrame.from_records(retVal)

        if len(df.columns):
            df.columns = ['t', 'o', 'l', 'h', 'c', 'v']
            df['t'] = pandas.to_datetime(df['t'], unit = 's')
            df.sort_index
              
        # generate returns for the day
        returns = []
        for i in range(0, len(candles)):
            if i == 0:
                returns = returns + [0]
            else:
                returns = returns + [(df.iloc[i]['c'] - df.iloc[i-1]['c'])/df.iloc[i-1]['c']]
        df['r'] = returns

        if debug and len(df.columns) > 0:
            print(df.describe())

        return df

    def get_historical_data(self, ticker, fn, time_period = 60, days = 90, debug = False, include_ah = False, pickle = True): 
        if self.jar == None:
            self.init_jar(ticker)
        historical_data = pandas.DataFrame()
        today = datetime.today()
        x_days_ago = today + timedelta(days = -1 * days)
        current_date = x_days_ago
        while current_date <= today:
            # look for pickle file for this days data for this day's ticker
            pickle_name = "{0}.{1}.{3}.{2}.pkl".format(ticker, time_period, current_date.strftime("%m-%d-%Y"),
                                                          fn.__name__)
            if pickle and self.jar.pickle_exists(pickle_name):
                data = self.jar.read_pickle_dataframe(pickle_name)
            else:
                data = fn(ticker, current_date, debug = debug, include_ah = include_ah, pickle = pickle)
                self.jar.write_pickle_dataframe(pickle_name, data)
            historical_data = historical_data.append(data)
            current_date = current_date + timedelta(days = 1)
        # label & type the data frame
        if len(historical_data.columns) == 6:
            historical_data.columns = ['t', 'o', 'l', 'h', 'c', 'v']
        elif len(historical_data.columns) == 7:
            historical_data.columns = ['t', 'o', 'l', 'h', 'c', 'v', 'r']
        historical_data['t'] = pandas.to_datetime(historical_data['t'], unit = 's')
        historical_data.index.name = 't'
        return historical_data
    
    def _api_call_with_sleep(self, fn, *args):
        result = fn(*args)
        time.sleep(self.sleep_for)
        return result