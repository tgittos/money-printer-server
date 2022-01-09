import os
import time
import requests
import redis
import json
import sseclient

from core.lib.logger import get_logger

from constants import BACKBONE_STONKS_CHANNEL, BACKBONE_WS_CHANNEL
from config import config


class SSEClient:

    redis = redis.Redis(host=config.redis.host, port=config.redis.port, db=0)
    headers = {
        'Connection': 'keep-alive',
        'Cache-Control': 'no-cache',
        'Accept': 'text/event-stream'
    }
    params = {
        'name': 'mp-data-server'
    }
    tracked_symbols = {}
    running = False

    def __init__(self, iexcloud_secret):
        self.logger = get_logger(__name__)
        self.secret_token = iexcloud_secret
        self.p = self.redis.pubsub()
        self.p.subscribe(**{BACKBONE_STONKS_CHANNEL: self._handle_redis_message})
        self.thread = self.p.run_in_thread(sleep_time=0.1)

    def start(self):
        self.logger.info("starting upstream sse connection")
        self.running = True
        while self.running:
            if len(self.tracked_symbols.keys()) > 0:
                url = self._gen_api_url(self.tracked_symbols.keys())
                self.logger.debug("starting stream to url: {0}".format(url))
                stream_response = requests.get(url, stream=True, headers=self.headers, params=self.params)
                client = sseclient.SSEClient(stream_response)
                for event in client.events():
                    event_data = event.data
                    # print(" * publishing event to upstream-symbols pubsub: {0}".format(event_data))
                    self._stream_data(event_data)
                    if not self.running:
                        break
            time.sleep(0.2)
        self.logger.info("stopping upstream sse connection")

    def stop(self):
        self.running = False
        if self.thread:
            self.thread.join()

    def restart(self):
        if self.running:
            self.stop()
        self.start()

    def subscribe(self, symbol):
        restart = False
        if symbol not in self.tracked_symbols:
            self.logger.debug("adding {0} to tracking list".format(symbol))
            self.tracked_symbols[symbol] = 0
            restart = True
        self.tracked_symbols[symbol] += 1
        if restart:
            self.restart()

    def unsubscribe(self, symbol):
        if symbol in self.tracked_symbols:
            self.tracked_symbols[symbol] -= 0
            if self.tracked_symbols[symbol] == 0:
                self.logger.debug("removing {0} from tracking list".format(symbol))
                del self.tracked_symbols[symbol]
                self.restart()

    def _handle_redis_message(self, redis_message):
        command, args = redis_message
        if command == 'subscribe':
            self.subscribe(args)
        if command == 'unsubscribe':
            self.unsubscribe(args)
        else:
            self.logger.debug(f"unrecognized command {command} with args {args}")

    def _stream_data(self, event_data):
        self.redis.publish(BACKBONE_WS_CHANNEL, json.dumps({
            'to': event_data['symbol'],
            **event_data
        }))

    def __gen_api_url(self, symbols):
        if os.environ['MP_ENVIRONMENT'] != 'production':
            url = "https://sandbox-sse.iexapis.com/stable/stocksUSNoUTP?symbols={0}&token={1}&chartIEXOnly=true"\
                .format(','.join(symbols), self.secret_token)
        else:
            url = "https://cloud-sse.iexapis.com/stable/stocksUSNoUTP?symbols={0}&token={1}&chartIEXOnly=true"\
                .format(','.join(symbols), self.secret_token)
        return url
