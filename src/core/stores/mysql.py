from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


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
    sessionmaker = None

    def __init__(self, config):
        if not MySql.engine or not MySql.sessionmaker:
            conn_str = "mysql://{0}:{1}@{2}:{3}/{4}".format(
                config.username,
                config.password,
                config.host,
                config.port,
                config.schema
            )
            self.engine = create_engine(conn_str, echo=config.debug)
            self.sessionmaker = sessionmaker(bind=self.engine)

    def get_session(self):
        session = self.sessionmaker()
        return session

    def with_session(self, expr):
        session = self.sessionmaker()
        res = expr(session)
        session.close()
        return res
