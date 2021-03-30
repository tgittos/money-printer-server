import sys
sys.path.append('./../../src')

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

import config

Base = declarative_base()

class Db:
    
    def __init__(self, echo=False):
        conn_str = "mysql://{0}:{1}@{2}:{3}/{4}".format(
            config.db['username'],
            config.db['password'],
            config.db['host'],
            config.db['port'],
            config.db['schema']
        )
        self.engine = create_engine(conn_str, echo=echo)
        self.session = sessionmaker(bind=self.engine)

    def get_session(self):
        return self.session()