import pytest
import os
from sqlalchemy_utils import database_exists

from config import mysql_config
from core.stores.mysql import MySql
from apps.api import ApiApplication

# hardcode test env when running tests
os.environ["MP_ENVIRONMENT"] = "test"


# one DB for the whole test session so that we can parallelize it
@pytest.fixture(scope='session')
def db(autouse=True):
    db = MySql(mysql_config)
    # if not database_exists(db.engine.url):
    #    db.create_all()
    db.create_all()
    yield db
    # if database_exists(db.engine.url):
    #    db.drop_all()
    db.drop_all()


# one API for the the whole test session so that we can parallelize it
@pytest.fixture(scope='session')
def client(db):
    app = ApiApplication(db)

    with app.flask_app.test_client() as client:
        with app.flask_app.app_context():
            yield client
