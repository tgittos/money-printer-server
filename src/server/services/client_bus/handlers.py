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

    def unsubscribe_symbols(self):
        print(" * shutting thread down")
        self.thread.stop()
        print(" * unsubscribing from upstream-symbols pubsub in thread")
        self.p.close()

    def __proxy(self, message):
        self.socketio.emit('upstream-symbols', json.dumps(message['data'].decode('utf-8')))

    def __augment_app(self):
        self.socketio.on_event('connect', self.connect)
        self.socketio.on_event('json', self.handle_json_message)
        self.socketio.on_event('subscribe_symbols', self.subscribe_symbols)
