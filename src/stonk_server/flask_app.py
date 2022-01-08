import os
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow

from core.lib.client_bus import ClientBus
from config import config
from .sse_client import SSEClient


app = Flask(__name__)
ma = Marshmallow(app)
cb = ClientBus()
sse = SSEClient(config.iex.secret)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = config.secret
CORS(app)