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
        self.tracked_symbols = []
        self.running = False

        self.redis = redis.Redis(host='localhost', port=6379, db=0)
        self.p = self.redis.pubsub()
        self.p.subscribe(**{'sse-control': self.__handle_sse_control})
        self.thread = self.p.run_in_thread(sleep_time=0.1)

    def start(self):
        print(" * starting upstream")
        self.running = True
        while self.running:
            if len(self.tracked_symbols) > 0:
                url = self.__gen_api_url(self.tracked_symbols)
                print(" * starting SSE stream to url: {0}".format(url))
                stream_response = requests.get(url, stream=True, headers=self.headers, params=self.params)
                client = sseclient.SSEClient(stream_response)
                for event in client.events():
                    event_data = event.data
                    # print(" * publishing event to upstream-symbols pubsub: {0}".format(event_data))
                    self.redis.publish('upstream-symbols', event_data)
                    message = self.p.get_message()
                    while message is not None:
                        self.__handle_sse_control(message)
                        message = self.p.get_message()
                    if not self.running:
                        break
            print(" * not tracking any symbols, sleep for 1s")
            time.sleep(1)
        print(" * stopping upstream")

    def stop(self):
        self.running = False

    def restart(self):
        self.running = False
        self.start()

    def __handle_sse_control(self, data):
        json_data = json.loads(data['data'])
        command = json_data['command']

        if command == "start":
            print(" * start command received, starting starting upstream server")
            self.start()
            return

        if command == "stop":
            print(" * stop command received, stopping upstream server")
            self.stop()
            return

        if command == "add-symbol":
            symbol = json_data['data']
            if symbol not in self.tracked_symbols:
                print(" * adding {0} to tracking list".format(symbol))
                self.tracked_symbols.append(symbol)

        elif command == "remove-symbol":
            symbol = json_data['data']
            if symbol in self.tracked_symbols:
                print(" * removing {0} from tracking list".format(symbol))
                self.tracked_symbols.remove(symbol)

        if self.running:
            self.stop()

        if len(self.tracked_symbols) > 0:
            self.start()

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
    print(" * data-server listening for commands")
