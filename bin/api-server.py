import os

import api.app as app
from api.lib.apispec import write_apispec
from config import mysql_config

if __name__ == '__main__':

    # create the app
    app.create_app()

    # generate docs when running in dev and staging
    if 'MP_ENVIRONMENT' in os.environ and \
        os.environ['MP_ENVIRONMENT'] == "development" or os.environ['MP_ENVIRONMENT'] == "staging":
        doc_path = os.path.dirname(__file__) + "/../docs/swagger/"
        write_apispec(doc_path + "swagger.json", app.app)

    app.run()
