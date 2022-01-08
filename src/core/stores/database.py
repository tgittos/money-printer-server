import os
from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session

from core.models.base import Base

from config import config

class Database(object):

    engine = None
    sm = None
    context = None

    def __init__(self, config):
        if not Database.engine or not Database.sm:
            conn_str = "postgresql://{0}:{1}@{2}:{3}/{4}".format(
                config.username,
                config.password,
                config.host,
                config.port,
                config.schema
            )
            Database.engine = create_engine(conn_str, echo=config.db.debug.lower()=='true')
            Database.sm = sessionmaker(
                bind=Database.engine, autoflush=True, expire_on_commit=False)

    def get_session(self):
        return Database.sm()

    def create_all(self):
        if os.environ['MP_ENVIRONMENT'] != 'test':
            raise Exception(
                "cannot call Database.create_all in a non-test environment")
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