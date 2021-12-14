from lxml import html
import requests
import json
import argparse
from collections import OrderedDict
from datetime import datetime

from lib.stonk_jar import StonkJar

import warnings
warnings.filterwarnings('ignore')

def get_fundamentals_data(ticker):
    last_fcf = get_free_cash_flow(ticker)
    shares = get_shares(ticker)
    eps, market_price = get_eps(ticker)
    ge = get_growth_estimate(ticker)

    return {'fcf': last_fcf, 'ge': ge, 'yr': 5, \
            'dr': 10, 'pr': 3, 'shares': shares, \
            'eps': eps, 'mp': market_price}

def dcf(ticker):
    pickle_name = "{0}.fundamentals-data.{1}-{2}.pkl".format(ticker, datetime.today().year, datetime.today().month)
    jar = StonkJar(ticker)
    data = jar.pickle_back(pickle_name, get_fundamentals_data, ticker)
    
    forecast = [data['fcf']]

    for i in range(1, data['yr']):
        forecast.append(forecast[-1] + (data['ge'] / 100) * forecast[-1])

    dcf = sum([forecast[i] / (1 + (data['dr'] / 100))**i for i in range(len(forecast))])
    final_value = forecast[-1] * (1 + (data['pr'] / 100)) / (data['dr'] / 100 - data['pr'] / 100)
    return final_value

def graham(ticker):
    pickle_name = "{0}.fundamentals-data.{1}-{2}.pkl".format(ticker, datetime.today().year, datetime.today().month)
    jar = StonkJar(ticker)
    data = jar.pickle_back(pickle_name, get_fundamentals_data, ticker)
    
    expected_value = data['eps'] * (8.5 + 2 * (data['ge']))
    ge_priced_in = (data['mp'] / data['eps'] - 8.5) / 2
    
    return { 'expected_value': expected_value, 'ge_priced_in': ge_priced_in }

def get_free_cash_flow(ticker):
    url = "https://stockanalysis.com/stocks/{}/financials/cash-flow-statement".format(ticker)
    response = requests.get(url, verify=False)
    parser = html.fromstring(response.content)
    fcfs = parser.xpath('//table[contains(@id,"fintable")]//tr[td/span/text()[contains(., "Free Cash Flow")]]')[0].xpath('.//td/text()')
    
    last_fcf = float(fcfs[0].replace(',', ''))
    return last_fcf

def get_growth_estimate(ticker):
    url = "https://in.finance.yahoo.com/quote/{}/analysis?p={}".format(ticker, ticker)
    response = requests.get(url, verify=False)
    parser = html.fromstring(response.content)
    ge = parser.xpath('//table//tbody//tr')

    for row in ge:
        label = row.xpath("td/span/text()")[0]
        if 'Next 5 years' in label:
            ge = float(row.xpath("td/text()")[0].replace('%', ''))
            break
    
    return ge

def get_shares(ticker):
    url = "https://stockanalysis.com/stocks/{}/".format(ticker)
    response = requests.get(url, verify=False)
    parser = html.fromstring(response.content)
    shares = parser.xpath('//div[@class="info"]//table//tbody//tr[td/text()[contains(., "Shares Out")]]')

    shares = shares[0].xpath('td/text()')[1]
    factor = 1000 if 'B' in shares else 1 
    shares = float(shares.replace('B', '').replace('M', '')) * factor
    
    return shares

def get_eps(ticker):
    url = "https://stockanalysis.com/stocks/{}/financials/".format(ticker)
    response = requests.get(url, verify=False)
    parser = html.fromstring(response.content)
    eps = parser.xpath('//table[contains(@id,"fintable")]//tr[td/span/text()[contains(., "EPS (Diluted)")]]')[0].xpath('.//td/text()')
    eps = float(eps[0])
    market_price = float(parser.xpath('//div[@id="sp"]/span[@id="cpr"]/text()')[0].replace('$', '').replace(',', ''))
    return [eps, market_price]