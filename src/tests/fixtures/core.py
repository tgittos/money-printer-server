import pytest
import os
from sqlalchemy import inspect
from sqlalchemy.sql import text

from config import mysql_config
from core.stores.mysql import MySql
from apps.api import ApiApplication

# hardcode test env when running tests
os.environ["MP_ENVIRONMENT"] = "test"


# one DB for the whole test session so that we can parallelize it
@pytest.fixture(scope='session')
def db(autouse=True):
    db = MySql(mysql_config)
    inspector = inspect(db.engine)
    if not inspector.has_table('alembic_version'):
        db.create_all()
    yield db
    truncate_db(db)


# one API for the the whole test session so that we can parallelize it
@pytest.fixture(scope='session')
def client(db):
    app = ApiApplication(db)

    with app.flask_app.test_client() as client:
        with app.flask_app.app_context():
            yield client

def truncate_db(db):
    script = """EOF
        SET FOREIGN_KEY_CHECKS = 0;

        SELECT @str := CONCAT('TRUNCATE TABLE ', table_schema, '.', table_name, ';')
        FROM   information_schema.tables
        WHERE  table_type   = 'BASE TABLE'
        AND  table_schema IN ('db1_name','db2_name');

        PREPARE stmt FROM @str;

        EXECUTE stmt;

        DEALLOCATE PREPARE stmt;

        SET FOREIGN_KEY_CHECKS = 1;
    """
    statement = text(script)
    with db.engine.connect() as connection:
        connection.execute(statement)
