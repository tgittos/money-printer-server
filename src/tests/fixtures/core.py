from flask.app import Flask
import pytest
from sqlalchemy import inspect

from core.stores.database import Database
from core.models import Base
from api.app import create_app

from config import config

# create an instance of the API clients once per python process
test_app, _ = create_app({ 'TESTING': True })

# one DB for the whole test session so that we can parallelize it
@pytest.fixture(scope='session')
def db():
    db = Database(config.api)
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
    with test_app.test_client() as client:
        with test_app.app_context():
            yield client
