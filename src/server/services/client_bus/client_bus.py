import json
import redis


class ClientBus:

    def __init__(self, socketio):
        self.r = redis.Redis(host='localhost', port=6379, db=0)
        self.p = self.r.pubsub()
        self.socketio = socketio
        self.__augment_app()
        self.thread = None

    def connect(self):
        print(" * client connected")

    def handle_json_message(self, data):
        print("received message: {0}".format(data))

    def get_symbols(self):
        print(" * requesting tracking state from upstream")
        if self.r is not None:
            self.r.publish('sse-control', json.dumps({
                'command': 'list-symbols'
            }))

    def subscribe_symbol(self, data=None):
        print(" * subscribing to upstream-symbols pubsub in thread: {0}".format(data))
        self.p.subscribe(**{'upstream-symbols': self.__proxy})
        self.thread = self.p.run_in_thread(sleep_time=0.1)
        if data is not None:
            self.r.publish('sse-control', json.dumps({
                'command': 'add-symbol',
                'data': data
            }))

    def unsubscribe_symbol(self, data=None):
        if self.p is not None:
            print(" * unsubscribing from upstream-symbols pubsub in thread")
            if data is not None:
                self.r.publish('sse-control', json.dumps({
                    'command': 'remove-symbol',
                    'data': data
                }))

    def fetch_historical_data(self, data=None):
        if self.p is not None:
            print(" * requesting historical data fetch using command {0}".format(data))
            if data is not None:
                self.r.publish('historical_quotes', json.dumps({
                    'command': 'fetch',
                    'data': data
                }))

    def __proxy(self, message):
        data_message = message['data'].decode('utf-8')
        # print(" * emitting event to upstream {0}".format(json_message))
        self.socketio.emit('live_quotes', data_message)

    def __augment_app(self):
        self.socketio.on_event('connect', self.connect)
        self.socketio.on_event('json', self.handle_json_message)
        self.socketio.on_event('subscribe_live_quotes', self.subscribe_symbol)
        self.socketio.on_event('live_quotes:tracking', self.get_symbols)
        self.socketio.on_event('live_quotes:subscribe-symbol', self.subscribe_symbol)
        self.socketio.on_event('live_quotes:unsubscribe-symbol', self.unsubscribe_symbol)
        self.socketio.on_event('unsubscribe_live_quotes', self.unsubscribe_symbol)
        self.socketio.on_event('historical_quotes:fetch', self.fetch_historical_data)
