import os
import sys
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

headers = { 'Accept': 'text/event-stream' }

print(" * starting SSE stream to url: {0}".format(url))
response = requests.get(url, stream=True, headers=headers)

print(" * got response from SSE stream: [{0}] {1}".format(response.status_code, response.text))
client = sseclient.SSEClient(response)

r = redis.Redis(host='localhost', port=6379, db=0)
for event in client.events():
    print(" * publishing event to upstream-symbols pubsub: {0}".format(event))
    redis.publish('upstream-symbols', event)
