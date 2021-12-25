import os

from api.apps.api import ApiApplication
from api.lib.apispec import write_apispec
from core.stores.mysql import MySql
from config import mysql_config

if __name__ == '__main__':
    doc_path = os.path.dirname(__file__) + "/../docs/swagger/"
    write_apispec(doc_path + "swagger.json")

    store = MySql(mysql_config)

    app = ApiApplication(store)
    app.run()
