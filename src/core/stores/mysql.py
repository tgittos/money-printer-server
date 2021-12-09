import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from core.models.base import Base


class MySqlConfig:
    def __init__(self, username, password, host, port, schema, debug=False):
        self.username = username
        self.password = password
        self.host = host
        self.port = port
        self.schema = schema
        self.debug = debug


class MySql:

    engine = None
    sm = None

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
            MySql.sm = sessionmaker(bind=MySql.engine, autoflush=True)

    def get_session(self):
        session = MySql.sm()
        return session

    def commit_session(self, session):
        session.commit()
        session.close()

    def with_session(self, expr):
        session = MySql.sm()
        res = expr(session)
        session.close()
        return res

    def create_all(self):
        if os.environ['MP_ENVIRONMENT'] != 'test':
            raise Exception("cannot call MySql.create_all in a non-test environment")
        connection = self.engine.connect()
        Base.metadata.bind = connection
        Base.metadata.create_all()

    def drop_all(self):
        if os.environ['MP_ENVIRONMENT'] != 'test':
            raise Exception("cannot call MySql.drop_all in a non-test environment")
        connection = self.engine.connect()
        Base.metadata.bind = connection
        Base.metadata.drop_all()
