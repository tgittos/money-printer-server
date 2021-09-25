from logging.config import fileConfig
import json
import os

from sqlalchemy import engine_from_config
from sqlalchemy import pool

from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# this will overwrite the ini-file sqlalchemy.url path
# with the path given in the config of the main code
env = 'development'
if 'MP_ENVIRONMENT' in os.environ:
    env = os.environ['MP_ENVIRONMENT']
f1 = open('./server/config.json',)
f2 = open('./server/.secrets.json',)
config_json = json.loads(f1.read())
secrets_json = json.loads(f2.read())
f1.close()
f2.close()

config.set_main_option('sqlalchemy.url',
                       "mysql://{0}:{1}@{2}:{3}/{4}".format(
                           secrets_json[env]['db']['username'],
                           secrets_json[env]['db']['password'],
                           config_json[env]['db']['host'],
                           config_json[env]['db']['port'],
                           config_json[env]['db']['schema']
                       ))

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)

# add your model's MetaData object here
# for 'autogenerate' support

import sys
print(" * path: {0}".format(sys.path))

from core.models.profile import Profile
from core.models.account import Account
from core.models.account_balance import AccountBalance
from core.models.holding_balance import HoldingBalance
from core.models.plaid_item import PlaidItem
from core.models.reset_token import ResetToken
from core.models.scheduled_job import ScheduledJob
from core.models.security import Security
from core.models.holding import Holding
from core.models.security_price import SecurityPrice
from core.models.iex_blacklist import IexBlacklist
from core.models.investment_transaction import InvestmentTransaction

from core.models.base import Base
target_metadata = Base.metadata

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode.

    In this scenario we need to create an Engine
    and associate a connection with the context.

    """
    connectable = engine_from_config(
        config.get_section(config.config_ini_section),
        prefix="sqlalchemy.",
        poolclass=pool.NullPool,
    )

    with connectable.connect() as connection:
        context.configure(
            connection=connection, target_metadata=target_metadata
        )

        with context.begin_transaction():
            context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
