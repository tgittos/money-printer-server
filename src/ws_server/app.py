
import re
from flask import Flask, request
from flask_socketio import SocketIO, join_room, leave_room
import redis
import os
import json

from core.lib.logger import init_logger, get_logger
from core.lib.client_bus import ClientBus
from auth.decorators import decode_jwt

from constants import BACKBONE_WS_CHANNEL, BACKBONE_STONKS_CHANNEL

log_path = os.path.dirname(__file__) + "/../../logs/"
init_logger(log_path)
logger = get_logger("server.services.ws_server")

app = Flask(__name__)

ws = SocketIO(app, cors_allowed_origins='*', message_queue="redis://")
cb = ClientBus()
conn_map = {}
reverse_conn_map = {}

@ws.on('connect')
def handle_connect(auth):
    """
    Authenticates a connection to ensure valid JWT token
    If connection is valid, request.sid is saved under the user's profile_id
    to allow direct to to user addressing from internal services
    """
    if 'bearer' in auth:
        token = auth['Bearer']
        profile = decode_jwt(token)
        if profile is not None:
            if profile.id not in conn_map:
                conn_map[profile.id] = []
            conn_map[profile.id].append(request.sid)
            reverse_conn_map[request.sid] = profile.id
            pass
    raise ConnectionRefusedError("Unauthorized")

@ws.on('disconnect')
def handle_disconnect():
    """
    Reaps the user's connection from their profile pool, and if the user's
    connection pool is empty, reaps them from the tracking map
    """
    profile_id = reverse_conn_map[request.sid]
    if profile_id in conn_map and request.sid in conn_map[profile_id]:
        conn_map[profile_id] = filter(lambda c: c != request.sid, conn_map[profile_id])
    if len(conn_map[profile_id]) == 0:
        del conn_map[profile_id]
    del reverse_conn_map[request.sid]

@ws.on('subscribe')
def handle_ws_subscribe(symbol):
    """
    Handles a `subscribe SPY` message from the web socket, and proxies it to
    the stonk service for subscription
    Joins a local room for the symbol, which the stonk service will address price
    updates to directly
    """
    join_room(symbol)
    cb.publish(BACKBONE_STONKS_CHANNEL, ('subscribe', symbol))

@ws.on('unsubscribe')
def handle_ws_unsubscribe(symbol):
    """
    Handles an `unsubscribe SPY` message from the websocket and proxies it to
    the stonk service for unsubscription.
    If other clients are subscribed, this will be a no-op in the stonk service
    Removes the connection from the local room to stop getting price updates.
    """
    leave_room(symbol)
    cb.publish(BACKBONE_STONKS_CHANNEL, ('unsubscribe', symbol))

@ws.on('json')
def handle_ws_message(ws_message):
    """
    Proxies a message from the ws directly to a backend service via the `to`
    property on the message.
    - 'stonks' for stock price server
    - 'api' for internal api requests (very rare)
    """
    e = ws_message['to']
    cb.publish(e, json.dumps(ws_message))

def handle_redis_message(redis_message):
    """
    Handles a generic message from redis received on the 'ws' channel
    If the data specifies a `to` (could be profile_id, request.sid, or symbol/room name),
    direct the message to the recepient.
    If the `to` is a profile_id, message _all_ connected clients
    """
    data = json.parse(redis_message['data'].decode())
    to = data['to']
    if to is not None and to in conn_map:
        conns = conn_map[to]
        for conn in conns:
            ws.send(data, json=True, to=conn)
    else:
        ws.send(data, json=True, to=to)


if __name__ == '__main__':
    cb.start()
    cb.subscribe(BACKBONE_WS_CHANNEL, handle_redis_message)
    ws.run(app, host=config.host, port=config.port)
    app.start()