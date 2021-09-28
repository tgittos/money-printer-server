import time
import requests
import redis
import json

import sseclient

from config import config
from core.lib.logger import get_logger


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
        self.logger = get_logger(__name__)
        self.env_string = env_string
        self.secret_token = iexcloud_secret
        self.tracked_symbols = []
        self.running = False

        self.redis = redis.Redis(host=config.redis.host, port=config.redis.port, db=0)
        self.p = self.redis.pubsub()
        self.p.subscribe(**{'sse-control': self.__handle_sse_control})
        self.thread = self.p.run_in_thread(sleep_time=0.1)

    def start(self):
        self.logger.info("starting upstream sse connection")
        self.running = True
        while self.running:
            if len(self.tracked_symbols) > 0:
                url = self.__gen_api_url(self.tracked_symbols)
                self.logger.debug("starting stream to url: {0}".format(url))
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
            time.sleep(0.2)
        self.logger.info("stopping upstream sse connection")

    def stop(self):
        self.running = False
        time.sleep(1)
        self.p.unsubscribe('sse-control')
        if self.thread:
            self.thread.join()

    def restart(self):
        self.stop()
        self.start()

    def __handle_sse_control(self, data):
        try:
            json_data = json.loads(data['data'])
            command = json_data['command']

            if command == "start":
                self.logger.debug("sse server received start command, requesting start of upstream")
                self.start()
                return

            if command == "stop":
                self.logger.debug("sse server received stop command, requesting stop of upstream")
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
                    self.logger.debug("adding {0} to tracking list".format(symbol))
                    self.tracked_symbols.append(symbol)

            elif command == "remove-symbol":
                symbol = json_data['data']
                if symbol in self.tracked_symbols:
                    self.logger.debug("removing {0} from tracking list".format(symbol))
                    self.tracked_symbols.remove(symbol)

            if self.running:
                self.stop()

            if len(self.tracked_symbols) > 0:
                self.start()
        except redis.exceptions.ConnectionError:
            # redis backbone connection terminated, shut ourselves down
            self.logger.exception("backbone redis connection dropped, shutting down")
            self.running = False

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
