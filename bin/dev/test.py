import os
import sys
import subprocess
from sqlalchemy.orm import declarative_base

from core.stores.mysql import MySql
from core.models import Base

from config import mysql_config

if __name__ == '__main__':
    db = MySql(mysql_config)
    print("Refreshing db table set...")
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)
    print("Running tests...")
    test_cmd = ["pytest", "-n", "auto", "--cov-config=.coveragerc", "--cov=src", "--cov-report", "term:skip-covered", "src/"]
    completed = subprocess.run(test_cmd)
    print("Dropping db table set...")
    Base.metadata.drop_all(bind=db.engine)
    print("Done")
    print(f"Exiting with code: {completed.returncode}")
    completed.check_returncode()
