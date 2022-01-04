import os
from sqlalchemy.orm import declarative_base

from api.lib.apispec import write_apispec
from api.app import create_app, app

if __name__ == '__main__':
    # create the app
    create_app()

    print("Writing updated OpenAPI spec file")
    doc_path = os.path.dirname(__file__) + "/../../docs/swagger/"
    write_apispec(doc_path + "swagger.json", app)
    print("Done")
