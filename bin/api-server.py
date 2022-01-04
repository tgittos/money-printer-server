import os

from api.app import create_app, run
from api.lib.apispec import write_apispec
from core.stores.mysql import MySql
from config import mysql_config

if __name__ == '__main__':

    store = MySql(mysql_config)

    # create the app
    create_app(store)

    # generate docs when running in dev and staging
    if 'MP_ENVIRONMENT' in os.environ and \
        os.environ['MP_ENVIRONMENT'] == "development" or os.environ['MP_ENVIRONMENT'] == "staging":
        doc_path = os.path.dirname(__file__) + "/../docs/swagger/"
        write_apispec(doc_path + "swagger.json", app)

    run()
