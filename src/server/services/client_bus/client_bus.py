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

    def subscribe_symbols(self, data):
        print(" * subscribing to upstream-symbols pubsub in thread")
        self.p.subscribe(**{'upstream-symbols': self.__proxy})
        self.thread = self.p.run_in_thread(sleep_time=0.1)
        self.r.publish('sse-control', json.dumps({
            'command': 'reset',
            'data': data
        }))

    def unsubscribe_symbols(self):
        if self.thread is not None:
            print(" * shutting thread down")
            self.thread.stop()
            self.thread.join()
        if self.p is not None:
            print(" * unsubscribing from upstream-symbols pubsub in thread")
            self.p.close()

    def __proxy(self, message):
        json_message = json.dumps(message['data'].decode('utf-8'))
        print(" * emitting event to upstream {0}".format(json_message))
        self.socketio.emit('live_quotes', json_message)

    def __augment_app(self):
        self.socketio.on_event('connect', self.connect)
        self.socketio.on_event('json', self.handle_json_message)
        self.socketio.on_event('subscribe_live_quotes', self.subscribe_symbols)
        self.socketio.on_event('unsubscribe_live_quotes', self.unsubscribe_symbols)
