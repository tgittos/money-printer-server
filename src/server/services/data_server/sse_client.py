import os
import sys
import signal
import time

import sseclient
import requests
import redis

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

secret_token = server_config[env_string]['iexcloud']['secret']

if env_string == 'sandbox':
    url = "https://sandbox-sse.iexapis.com/stable/stocksUS?symbols=spy&token={0}".format(secret_token)
else:
    url = "https://cloud-sse.iexapis.com/stable/stocksUS?symbols=spy&token={0}".format(secret_token)

headers = {
    'Connection': 'keep-alive',
    'Cache-Control': 'no-cache',
    'Accept': 'text/event-stream'
}

params = {
    'name': 'mp-data-server'
}

r = redis.Redis(host='localhost', port=6379, db=0)


while True:
    print(" * starting SSE stream to url: {0}".format(url))
    stream_response = requests.get(url, stream=True, headers=headers, params=params)
    client = sseclient.SSEClient(stream_response)

    for event in client.events():
        event_data = event.data
        print(" * publishing event to upstream-symbols pubsub: {0}".format(event_data))
        r.publish('upstream-symbols', event_data)

    print(" * connection reset, sleep for 1 min")
    time.sleep(60)
