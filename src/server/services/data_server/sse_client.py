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

    def __init__(self, env_string, iexcloud_secret):
        self.env_string = env_string
        self.secret_token = iexcloud_secret
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
                    self.__stream_data(event_data)
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
        # sleep for a few ticks to allow the redis pubsub to pick up that we're shutting down
        time.sleep(0.2)

    def restart(self):
        self.stop()
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

        if command == "list-symbols":
            self.redis.publish('upstream-symbols', json.dumps({
                'command': 'list-symbols',
                'data': self.tracked_symbols
            }))

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

    def __stream_data(self, event_data):
        self.redis.publish('upstream-symbols', json.dumps({
            'command': 'live-quote',
            'data': event_data
        }))

    def __gen_api_url(self, symbols):
        if self.env_string == 'sandbox':
            url = "https://sandbox-sse.iexapis.com/stable/stocksUSNoUTP?symbols={0}&token={1}&chartIEXOnly=true"\
                .format(','.join(symbols), self.secret_token)
        else:
            url = "https://cloud-sse.iexapis.com/stable/stocksUSNoUTP?symbols={0}&token={1}&chartIEXOnly=true"\
                .format(','.join(symbols), self.secret_token)
        return url
