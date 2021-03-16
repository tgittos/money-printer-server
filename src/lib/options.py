from math import log, sqrt, pi, exp
from scipy.stats import norm
from datetime import datetime, date, timedelta
import numpy as np
import pandas as pd
from pandas import DataFrame
import pandas_datareader.data as web

from lib.finnhub.data import FinnhubData as fh
from lib.yahoo.data import get_tnx

class Options:
    
    def __init__(self):
        self.fh = fh()
    
    def bs_call(self, S,K,T,r,sigma):
        return S * norm.cdf(self._d1(S, K, T, r, sigma)) - K * exp(-r*T) * norm.cdf(self._d2(S, K, T, r, sigma))
  
    def bs_put(self, S,K,T,r,sigma):
        return K * exp(-r*T) - S + self.bs_call(S, K, T, r, sigma)
    
    def call_forecast(self, ticker, strike, expiry, std_devs = 1):
        today = datetime.today()
        data = self.fh.get_historical_data(ticker, self.fh.stock_candles_by_date)
        dte = (datetime.strptime(expiry, "%m-%d-%Y") - today).days
        last_close = data.tail(1)['c']
        lower_b = last_close - (data['c'].std() * std_devs)
        upper_b = last_close + (data['c'].std() * std_devs)
        closes = np.linspace(lower_b, upper_b, dte)
        closes = [item for sublist in closes for item in sublist]
        uty = get_tnx()
        sigma = self.sigma(ticker)

        price_matrix = pd.DataFrame()
        for i in range(0, dte):
            l_t = (dte - i) / 365
            expiry_prices = []
            for j in closes:
                price = self.bs_call(j, strike, l_t, uty, sigma)
                expiry_prices = expiry_prices + [{'t': today + timedelta(days=i), 'c': j, 'v': price}]
            price_matrix = price_matrix.append(expiry_prices)

        price_matrix = price_matrix.pivot(index='t',columns='c', values='v')
        
        return price_matrix

    def sigma(self, ticker):
        data = self.fh.get_historical_data(ticker, self.fh.stock_candles_by_date)
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