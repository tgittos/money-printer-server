import json
import redis

from config import config
from core.lib.logger import get_logger


class ClientBus:

    running = False
    redis = None
    pubsub = None

    def __init__(self, socketio):
        self.logger = get_logger(__name__)
        self.socketio = socketio
        self.__augment_app()
        self.thread = None

    def start(self):
        self.logger.info("subscribing to upstream-symbols pubsub in thread")
        try:
            self.redis = redis.Redis(host=config.redis.host, port=config.redis.port, db=0)
            self.pubsub = self.redis.pubsub()
            self.pubsub.subscribe(**{'upstream-symbols': self.__proxy})
            self.thread = self.pubsub.run_in_thread(sleep_time=0.1)
            self.running = True
        except Exception as err:
            print(" error starting client bus: {0}".format(err))

    def stop(self):
        if self.thread and self.running:
            self.running = False
            self.pubsub.unsubscribe(**{'upstream-symbols': self.__proxy})
            self.thread.join()

    def connect(self):
        self.logger.debug("client connected")

    def handle_json_message(self, data):
        self.logger.debug("received message: {0}".format(data))

    def get_symbols(self):
        self.logger.debug("requesting tracking state from upstream")
        if self.redis is not None:
            self.redis.publish('sse-control', json.dumps({
                'command': 'list-symbols'
            }))

    def subscribe_symbol(self, data=None):
        if data is not None:
            self.redis.publish('sse-control', json.dumps({
                'command': 'add-symbol',
                'data': data
            }))

    def unsubscribe_symbol(self, data=None):
        self.logger.info("unsubscribing from upstream-symbols pubsub in thread")
        if data is not None:
            self.redis.publish('sse-control', json.dumps({
                'command': 'remove-symbol',
                'data': data
            }))

    def fetch_historical_data(self, data=None):
        self.logger.debug("requesting historical data fetch using command {0}".format(data))
        if data is not None:
            self.redis.publish('historical_quotes', json.dumps({
                'command': 'fetch',
                'data': data
            }))

    def __proxy(self, message):
        try:
            data_message = message['data'].decode('utf-8')
            # self.logger.debug("emitting event to upstream {0}".format(json_message))
            self.socketio.emit('live_quotes', data_message)
        except redis.exceptions.ConnectionError:
            # redis backbone connection terminated, shut ourselves down
            self.logger.exception("backbone redis connection dropped, shutting down")
            self.running = False

    def __augment_app(self):
        self.socketio.on_event('connect', self.connect)
        self.socketio.on_event('json', self.handle_json_message)
        self.socketio.on_event('subscribe_live_quotes', self.subscribe_symbol)
        self.socketio.on_event('live_quotes:tracking', self.get_symbols)
        self.socketio.on_event('live_quotes:subscribe-symbol', self.subscribe_symbol)
        self.socketio.on_event('live_quotes:unsubscribe-symbol', self.unsubscribe_symbol)
        self.socketio.on_event('unsubscribe_live_quotes', self.unsubscribe_symbol)
        self.socketio.on_event('historical_quotes:fetch', self.fetch_historical_data)
