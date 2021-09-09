from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class MySql:
    
    def __init__(self, config):
        conn_str = "mysql://{0}:{1}@{2}:{3}/{4}".format(
            config['username'],
            config['password'],
            config['host'],
            config['port'],
            config['schema']
        )
        self.engine = create_engine(conn_str, echo=config['debug'])
        self.session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.session()
