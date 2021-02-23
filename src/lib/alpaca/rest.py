import enum
import requests

import config

def auth():
    [alpaca_url, alpaca_key, alpaca_secret] = load_config()

    auth_url = "{0}/v2/account".format(alpaca_url)

    headers = dict()
    headers["APCA-API-KEY-ID"] = alpaca_key
    headers["APCA-API-SECRET-KEY"] = alpaca_secret

    response = requests.get(url = auth_url, headers = headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(response)
        return None

def last_quote(ticker):
    [alpaca_url, alpaca_key, alpaca_secret] = load_config()

    ticker.lower()
    api_url = "{0}/v1/last_quote/stocks/{1}".format(alpaca_url, ticker)

    headers = dict()
    headers["APCA-API-KEY-ID"] = alpaca_key
    headers["APCA-API-SECRET-KEY"] = alpaca_secret

    response = requests.get(url = api_url, headers = headers)

    if response.status_code == 200:
        return response.json()
    else:
        print(response)
        return None

def last_trade(ticker):
    [alpaca_url, alpaca_key, alpaca_secret] = load_config()

    ticker.lower()
    api_url = "{0}/v1/last/stocks/{1}".format(alpaca_url, ticker)

    headers = dict()
    headers["APCA-API-KEY-ID"] = alpaca_key
    headers["APCA-API-SECRET-KEY"] = alpaca_secret

    response = requests.get(url = api_url, headers = headers)
    print(api_url)
    print(response)

    if response.status_code == 200:
        return response.json()
    else:
        print(response)
        return None

class Timeframe:
    minute = '1Min'
    five_minute = '5Min'
    fifteen_minute = '15Min'
    day = '1D'

def bars(tickers, timeframe):
    [alpaca_url, alpaca_key, alpaca_secret] = load_config()

    symbols = ",".join(tickers)
    symbols = symbols.lower()

    api_url = "{0}/v1/bars/{1}?limit=100&symbols={2}".format(alpaca_url,
            timeframe, symbols)

    headers = dict()
    headers["APCA-API-KEY-ID"] = alpaca_key
    headers["APCA-API-SECRET-KEY"] = alpaca_secret

    response = requests.get(url = api_url, headers = headers)
    print(api_url)
    print(response)

    if response.status_code == 200:
        return response.json()
    else:
        print(response)
        return None

def load_config():
    alpaca_url = config.api_urls['alpaca']['data']
    alpaca_key = config.api_keys['alpaca']['paper']['key_id']
    alpaca_secret = config.api_keys['alpaca']['paper']['secret']
    return [alpaca_url, alpaca_key, alpaca_secret]
