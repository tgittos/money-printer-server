from math import log, sqrt, pi, exp
from scipy.stats import norm
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame
import pandas_datareader.data as web

from lib.stores.mysql import Mysql
from lib.yahoo.data import get_tnx

class Options:
    
    def __init__(self):
        self.mysql = Mysql()
    
    def call_exit_window(self, ticker, strike, expiry, cost, std_devs = 1):
        price_matrix = self.call_forecast(ticker, strike, expiry, std_devs)
        max_price = price_matrix.max().max()
        median_price = price_matrix.median().median()
        return [median_price, max_price]
    
    def call_entry_window(self, ticker, strike, expiry, std_devs = 1):
        price_matrix = self.call_forecast(ticker, strike, expiry, std_devs)
        min_price = (price_matrix.median() - (price_matrix.std() * std_devs)).median()
        median_price = price_matrix.median().median()
        return [min_price, median_price]

    def put_exit_window(self, ticker, strike, expiry, cost, std_devs = 1):
        price_matrix = self.put_forecast(ticker, strike, expiry, std_devs)
        max_price = price_matrix.max().max()
        median_price = price_matrix.median().median()
        return [median_price, max_price]
    
    def put_entry_window(self, ticker, strike, expiry, std_devs = 1):
        price_matrix = self.put_forecast(ticker, strike, expiry, std_devs)
        min_price = (price_matrix.median() - (price_matrix.std() * std_devs)).median()
        median_price = price_matrix.median().median()
        return [min_price, median_price]

    def bs_call(self, S,K,T,r,sigma):
        return S * norm.cdf(self._d1(S, K, T, r, sigma)) - K * exp(-r*T) * norm.cdf(self._d2(S, K, T, r, sigma))
  
    def bs_put(self, S,K,T,r,sigma):
        return K * exp(-r*T) - S + self.bs_call(S, K, T, r, sigma)
    
    def call_forecast(self, ticker, strike, expiry, std_devs = 1):
        return self._forecast(ticker, strike, expiry, self.bs_call, std_devs)
    
    def put_forecast(self, ticker, strike, expiry, std_devs = 1):
        return self._forecast(ticker, strike, expiry, self.bs_put, std_devs)

    def sigma(self, ticker):
        data = self.mysql.get_closes_by_symbol(ticker)
        returns = []
        for i in range(0, len(data)):
            if i == 0:
                returns = returns + [0]
            else:
                returns = returns + [(data.iloc[i]['c'] - data.iloc[i-1]['c'])/data.iloc[i-1]['c']]
        data['r'] = returns
        return np.sqrt(252) * data['r'].std()
    
    def _d1(self, S, K, T, r, sigma):
        return(log(S/K) + (r+sigma**2/2.) * T) / sigma*sqrt(T)
    
    def _d2(self, S, K, T, r, sigma):
        return self._d1(S, K, T, r, sigma)-sigma*sqrt(T)
    
    def _forecast(self, ticker, strike, expiry, fn, std_devs = 1):
        today = datetime.today()
        data = self.mysql.get_candles_by_symbol(ticker, 60)
        dte = (datetime.strptime(expiry, "%m-%d-%Y") - today).days+1
        last_close = data.tail(1)['c']
        lower_b = last_close - (data['c'].std() * std_devs)
        upper_b = last_close + (data['c'].std() * std_devs)
        closes = np.linspace(lower_b, upper_b, 10)
        closes = [item for sublist in closes for item in sublist]
        uty = get_tnx()
        sigma = self.sigma(ticker)

        price_matrix = pd.DataFrame()
        
        for i in range(0, dte+1):
            l_t = (dte - i) / 365
            expiry_prices = []
            for j in closes:
                price = fn(j, strike, l_t, uty, sigma)
                expiry_prices = expiry_prices + [{'t': today + timedelta(days=i), 'c': j, 'v': price}]
            price_matrix = price_matrix.append(expiry_prices)

        price_matrix = price_matrix.pivot(index='t',columns='c', values='v')
        
        return price_matrix