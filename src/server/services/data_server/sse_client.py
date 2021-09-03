import os
import sys
import signal
import time
import requests
import redis
import json

import sseclient


class SSEClient:

    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Accept': 'text/event-stream'
    }
    params = {
        'name': 'mp-data-server'
    }

    def __init__(self):
        self.secret_token = server_config[env_string]['iexcloud']['secret']
        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.p = self.redis.pubsub()
        self.p.subscribe(**{'sse-control': self.__track_symbol})
        self.thread = self.p.run_in_thread(sleep_time=0.1)
        self.tracked_symbols = []
        self.halt = False

    def start(self):
        while not self.halt:
            if len(self.tracked_symbols) > 0:
                url = self.__gen_api_url(self.tracked_symbols)
                print(" * starting SSE stream to url: {0}".format(url))
                stream_response = requests.get(url, stream=True, headers=self.headers, params=self.params)
                client = sseclient.SSEClient(stream_response)
                for event in client.events():
                    if self.halt:
                        break
                    event_data = event.data
                    print(" * publishing event to upstream-symbols pubsub: {0}".format(event_data))
                    self.redis.publish('upstream-symbols', event_data)
            print(" * not tracking any symbols, sleep for 1s")
            time.sleep(1)
        print(" * stopping SSE stream")

    def stop(self):
        self.halt = True

    def restart(self):
        self.halt = False
        self.start()

    def __track_symbol(self, data):
        json_data = json.loads(data['data'])
        for symbol in json_data['data']:
            if symbol not in self.tracked_symbols:
                self.tracked_symbols.append(symbol)
        self.halt = True
        print(" * restarting SSE server")
        self.restart()

    def __gen_api_url(self, symbols):
        if env_string == 'sandbox':
            url = "https://sandbox-sse.iexapis.com/stable/stocksUS1Second?symbols={0}&token={1}"\
                .format(','.join(symbols), self.secret_token)
        else:
            url = "https://cloud-sse.iexapis.com/stable/stocksUS1Second?symbols={0}&token={1}"\
                .format(','.join(symbols), self.secret_token)
        return url


if __name__ == '__main__':
    # echo the environment we're passing in
    env_string = os.environ['MONEY_PRINTER_ENV']
    print(" * setting env to {0}".format(env_string))

    # sometimes we run with whacky paths, so lets set the python runtime
    # pwd to something sane
    pwd = os.path.abspath(os.path.dirname(__file__) + "/../../../")

    print(" * changing pwd to {0}".format(pwd))
    os.chdir(pwd)

    # also add the core dir to the path so we can include from it
    print(" * augmenting path with core")
    sys.path.append(pwd)
    print(" * path: {0}".format(sys.path))

    from server.config import config as server_config

    sse_client = SSEClient()
    sse_client.start()
