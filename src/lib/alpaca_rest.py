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
        return None
