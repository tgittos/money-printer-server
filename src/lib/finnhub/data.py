import sys
sys.path.append('./../../src')

from os import path
from datetime import date, datetime, timedelta
import time
import calendar
import finnhub
import pandas

from urllib3.exceptions import ReadTimeoutError

import config

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

    def __init__(self):
        self.finnhub_client = finnhub.Client(api_key=config.api_keys['finnhub']['live'])
        self.sleep_for = 3

    def recommendation_trends_by_date(self, ticker, date, debug = False):
        first_of_month = date.replace(day = 1)
        recommendations = self.api_call_with_sleep(self.finnhub_client.recommendation_trends, ticker)    
        recommendation = [r for r in recommendations if datetime.strptime(r['period'], '%Y-%m-%d').date() == first_of_month]
        if (len(recommendation) > 0):
            return recommendation[0]
        return {}

    def company_earnings_by_date(self, ticker, date, debug = False):
        reporting_period = timedelta(days = 90)
        earnings = self.finnhub_client.company_earnings(ticker)   
        earning = [r for r in earnings if datetime.strptime(r['period'], '%Y-%m-%d').date() + reporting_period > date]
        if (len(earning) > 0):
            return earning[0]
        return {}

    def stock_candles_by_date(self, ticker, date, time_period = 60, debug = False):
        start_date = date.replace(hour=0, minute=0, second=0, microsecond=0)
        start_ts = int(start_date.timestamp())
        end_ts = int((start_date + timedelta(days=1)).timestamp())

        if debug:
            print("[stock_candles_by_date] fetching market candles")
        
        candles = self._api_call_with_sleep(self.finnhub_client.stock_candles, ticker, time_period, start_ts, end_ts)

        if 's' in candles and candles['s'] == 'no_data':
            return pandas.DataFrame()

        candle_rows = list(zip(candles['t'], candles['l'], candles['o'], candles['c'], candles['h'], candles['v']))    
        df = pandas.DataFrame.from_records(candle_rows)
              
        # generate returns for the day
        returns = []
        for i in range(0, len(candle_rows)):
            if i == 0:
                returns = returns + [0]
            else:
                returns = returns + [(df.iloc[i][4] - df.iloc[i-1][4])/df.iloc[i-1][4]]
                
        df['r'] = returns
        
        df.columns = ['t', 'o', 'l', 'h', 'c', 'r', 'v']
        df['t'] = pandas.to_datetime(df['t'], unit = 's')
        df.sort_index

        if debug and len(df.columns) > 0:
            print(df.describe())

        return df

    def get_historical_data(self, ticker, fn, time_period = 60, days = 365, debug = False): 
        historical_data = pandas.DataFrame()
        today = datetime.today()
        x_days_ago = today + timedelta(days = -1 * days)
        current_date = x_days_ago
        try:
            while current_date <= today:
                # skip weekends
                if current_date.weekday() < 5:
                    data = fn(ticker, current_date, time_period, debug = debug)
                    historical_data = historical_data.append(data)
                current_date = current_date + timedelta(days = 1)
        except ReadTimeoutError:
            # catch it and continue with the data we have
            print("read timeout fetching {0} symbol, {1} resolution, {2} day".format(
                ticker,
                time_period,
                current_date
            ))
        # label & type the data frame
        if len(historical_data.columns) == 6:
            historical_data.columns = ['t', 'o', 'l', 'h', 'c', 'v']
        elif len(historical_data.columns) == 7:
            historical_data.columns = ['t', 'o', 'l', 'h', 'c', 'r', 'v']
        historical_data['t'] = pandas.to_datetime(historical_data['t'], unit = 's')
        historical_data.index.name = 't'
        return historical_data
    
    def _api_call_with_sleep(self, fn, *args):
        result = fn(*args)
        time.sleep(self.sleep_for)
        return result