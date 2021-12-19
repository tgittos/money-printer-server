import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from core.models.base import Base


class MySqlConfig:
    def __init__(self, username, password, host, port, schema, debug=False):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.schema = schema
        self.debug = debug

class MySql(object):

    engine = None
    sm = None
    context = None

    def __init__(self, config):
        if not MySql.engine or not MySql.sm:
            conn_str = "mysql://{0}:{1}@{2}:{3}/{4}".format(
                config.username,
                config.password,
                config.host,
                config.port,
                config.schema
            )
            MySql.engine = create_engine(conn_str, echo=config.debug)
            MySql.sm = sessionmaker(
                bind=MySql.engine, autoflush=True, expire_on_commit=False)

    def get_session(self):
        return MySql.sm()

    def create_all(self):
        if os.environ['MP_ENVIRONMENT'] != 'test':
            raise Exception(
                "cannot call MySql.create_all in a non-test environment")
        connection = self.engine.connect()
        Base.metadata.bind = connection
        Base.metadata.create_all()

    def drop_all(self):
        if os.environ['MP_ENVIRONMENT'] != 'test':
            raise Exception(
                "cannot call MySql.drop_all in a non-test environment")
        connection = self.engine.connect()
        Base.metadata.bind = connection
        Base.metadata.drop_all()