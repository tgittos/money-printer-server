import pytest

from server.services.api.apps.api import ApiApplication
from core.stores.mysql import MySql
from config import mysql_config


@pytest.fixture
def db():
    db = MySql(mysql_config)
    db.create_all()
    yield db
    db.drop_all()


@pytest.fixture(scope='session')
def client():
    db = MySql(mysql_config)
    app = ApiApplication(db)

    db.create_all()

    with app.flask_app.test_client() as client:
        with app.flask_app.app_context():
            yield client

    db.drop_all()
