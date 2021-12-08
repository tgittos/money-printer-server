import os
import tempfile

import pytest

from server.services.api.application import ApiApplication
from flaskr.db import init_db


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({'TESTING': True, 'DATABASE': db_path})

    with app.test_client() as client:
        with app.app_context():
            init_db()
        yield client

    os.close(db_fd)
    os.unlink(db_path)

@pytest.fixture(scope='session')
def session_factory(engine)

@pytest.fixture
def session(db_session_factory=):
