import os

from api.app import create_app
from api.lib.apispec import write_apispec
from config import mysql_config

if __name__ == '__main__':

    # create the app
    app, ma, cb, ws = create_app()

    # generate docs when running in dev and staging
    if 'MP_ENVIRONMENT' in os.environ:
        os.environ['FLASK_ENV'] = os.environ['MP_ENVIRONMENT']
        if os.environ['MP_ENVIRONMENT'] == "development" or os.environ['MP_ENVIRONMENT'] == "staging":
            doc_path = os.path.dirname(__file__) + "/../docs/swagger/"
            write_apispec(doc_path + "swagger.json", app)
    
    # always run on the public port, cause we're in a container
    app.run(host='0.0.0.0')
