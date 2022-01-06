import os
import sys
import subprocess
from multiprocessing import Pool
from sqlalchemy.orm import declarative_base

from core.stores.mysql import MySql
from core.models import Base

from config import mysql_config

def run_test():
    test_cmd = ["pytest", "-n", "auto", "--cov-config=.coveragerc",
                "--cov=src", "--cov-report", "term:skip-covered", "src/"]
    if 'MP_CI' in os.environ:
        completed = subprocess.run(test_cmd, capture_output=True)
    else:
        completed = subprocess.run(test_cmd)
    return completed


if __name__ == '__main__':
    db = MySql(mysql_config)
    print("Refreshing db table set...")
    Base.metadata.drop_all(bind=db.engine)
    Base.metadata.create_all(bind=db.engine)
    print("Running tests...")
    # pool = Pool(processes=1)
    # completed = pool.apply_async(run_test)
    completed = run_test()
    print("Dropping db table set...")
    Base.metadata.drop_all(bind=db.engine)
    print("Done")
    if 'MP_CI' in os.environ:
        print(completed.stdout.decode())
        print(completed.stdout.decode())
        completed.check_returncode()