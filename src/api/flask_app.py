import os
from flask import Flask
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from core.stores.database import Database
from api import logger
from config import config


if 'MP_ENVIRONMENT' in os.environ:
    os.environ['FLASK_ENV'] = os.environ['MP_ENVIRONMENT']

logger.debug("* initializing Flask, Marshmallow and Client Bus")
app = Flask(__name__)
ma = Marshmallow(app)
db = Database(config.api)

app.config['CORS_HEADERS'] = 'Content-Type'
app.config['SECRET_KEY'] = config.secret
CORS(app)