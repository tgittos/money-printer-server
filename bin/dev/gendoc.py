import os
from sqlalchemy.orm import declarative_base

from api.lib.apispec import write_apispec

if __name__ == '__main__':
    print("Writing updated OpenAPI spec file")
    doc_path = os.path.dirname(__file__) + "/../../docs/swagger/"
    write_apispec(doc_path + "swagger.json")
    print("Done")
