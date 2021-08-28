import sys
sys.path.append('../../')

import websocket
import threading
import time
import json

import lib.tickers as tickers

class FinnhubWebsocket:

    def __init__(self):
        self.ws_url = "wss://ws.finnhub.io"
        self.ws = None

        self.cancel = False
        self.authenticating = False
        self.authenticated = False
        self.listening = False

        self.ticker_callback = None
        self.verbose = False
        self.tickers = []

        self.load_config()

    def set_verbose(self, val):
        self.verbose = val
        if (self.verbose == True):
            websocket.enableTrace(True)
            print("-- verbose mode on --")

    def set_tickers(self, tickers):
        self.tickers = tickers
        if (self.verbose == True):
            print("-- setting tickers --\n{0}".format(tickers))

    def start_stream(self):
        if (self.ws == None):
            self.init_stream()
        if (self.verbose == True):
            print("-- starting websocket --")
        self.ws.run_forever()

    def stop_stream(self):
        cancel = True

    def init_stream(self):
        if (self.verbose == True):
            print("-- initializing websocket --")

        # gross? - trying to capture 'self', currying didnt work
        def ws_m(ws, msg):
            self.ws_on_message(ws, msg)
        def ws_e(ws, error):
            self.ws_on_error(ws, error)
        def ws_c(ws):
            self.ws_on_close(ws)
        def ws_o(ws):
            self.ws_on_open(ws)

        self.ws = websocket.WebSocketApp(self.ws_url,
            on_message = ws_m,
            on_error = ws_e,
            on_close = ws_c)
        self.ws.on_open = ws_o

    def ws_on_message(self, ws, message):
        json_msg = json.loads(message);
        if (json_msg["stream"] == "authorization"):
            if (json_msg["data"]["action"] == "authenticate" and json_msg["data"]["status"] == "authorized"):
                if (self.verbose == True):
                    print("-- successfully authenticated with Alpaca! --")
                self.authenticated = True
        else:
            if (self.ticker_callback != None):
                self.ticker_callback(message)

    def ws_on_error(self, ws, error):
        print(error)

    def ws_on_close(self, ws):
        authenticated = False

    def ws_on_open(self, ws):
        if self.verbose == True:
            print("-- ws opened --")
        def run(*args):
            while self.cancel == False:
                if (self.authenticating == False and self.authenticated == False):
                    self.authenticating = True
                    self.ws_auth()
                if (self.authenticated == True and self.listening == False and len(self.tickers) > 0):
                    self.ws_listen(self.tickers)
                time.sleep(1) # 1 second
            if (self.verbose == True):
                print("-- cancel detected, closing ws --")
            self.ws.close()
            if (self.verbose == True):
                print("-- joining thread to end --")
            self.thread.join()
        if (self.verbose == True): 
            print("-- starting listening thread --")
        self.thread = threading.Thread(target=run, args=())
        self.thread.start()

    def ws_auth(self):
        if (self.verbose):
            print('-- authenticating with Alpaca --')
        data = {
            "action": "authenticate",
            "data": {
                "key_id": self.alpaca_key,
                "secret_key": self.alpaca_secret
            }
        }
        self.ws.send(json.dumps(data))

    def ws_listen(self, tickers):
        if (self.verbose):
            print("-- listening for the following tickers: {0} --".format(tickers))
        streams = []
        for ticker in tickers:
            ticker = ticker.upper()
            streams = streams + [
                "T.{0}".format(ticker),
                "Q.{0}".format(ticker),
                "AM.{0}".format(ticker)
            ]

        data =  {
            "action": "listen",
            "data": {
                "streams": streams
            }
        }
           
        if (self.verbose):
            print("-- sending listen message to Alpaca --")
            print(data)

        self.ws.send(json.dumps(data))
        self.listening = True

if __name__ == "__main__":
    print("-- starting in ticker mode --")

    tracking_tickers = tickers.get_tickers()

    client = AlpacaWebsocket()
    client.set_verbose(False)

    def print_ticker(msg):
        print(msg)

    client.ticker_callback = print_ticker
    client.set_tickers(tracking_tickers)

    client.start_stream()
