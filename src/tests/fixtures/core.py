from flask.app import Flask
import pytest
from sqlalchemy import inspect

from core.stores.database import Database
from core.models import Base
from api.app import app, create_app

from config import config

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
    create_app({ 'TESTING': True })
    with app.test_client() as client:
        with app.app_context():
            yield client
