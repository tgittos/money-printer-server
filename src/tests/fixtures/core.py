import pytest
from sqlalchemy import inspect

from core.stores.mysql import MySql
from core.models import Base

from apps.api import ApiApplication

from config import mysql_config

# one DB for the whole test session so that we can parallelize it


@pytest.fixture(scope='session')
def db():
    db = MySql(mysql_config)
    inspector = inspect(db.engine)
    created = False
    if not inspector.has_table('profiles'):
        Base.metadata.create_all(bind=db.engine)
        created = True
    yield db
    if created:
        Base.metadata.drop_all(bind=db.engine)


# one API for the the whole test session so that we can parallelize it
@pytest.fixture(scope='session')
def client(db):
    app = ApiApplication(db)

    with app.flask_app.test_client() as client:
        with app.flask_app.app_context():
            yield client
