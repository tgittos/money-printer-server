import os

from server.config import config as server_config


def load_config():
    env_string = "sandbox"
    if 'MONEY_PRINTER_ENV' in os.environ:
        env_string = os.environ['MONEY_PRINTER_ENV']

    if env_string == "production":
        return server_config['production']
    if env_string == "staging":
        return server_config['staging']
    if env_string == "development":
        return server_config['development']

    return server_config['sandbox']
