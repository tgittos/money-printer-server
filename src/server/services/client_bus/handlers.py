
def connect():
    print("ws client connected")


def handle_json_message(data):
    print("received message: {0}".format(data))


def subscribe_symbols(data):
    print("received subscribe_symbols message: {0}".format(data))


def augment_app(socketio):
    socketio.on_event('connect', connect)
    socketio.on_event('json', handle_json_message)
    socketio.on_event('subscribe_symbols', subscribe_symbols)
