from server.services.api.apps.api import ApiApplication
from core.stores.mysql import MySql
from config import mysql_config

if __name__ == '__main__':
    store = MySql(mysql_config)
    app = ApiApplication(store)
    app.run()
