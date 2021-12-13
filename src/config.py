import os
from dynaconf import Dynaconf

from core.apis.mailgun import MailGunConfig
from core.stores.mysql import MySqlConfig

env = 'development'
if 'MP_ENVIRONMENT' in os.environ:
    env = os.environ['MP_ENVIRONMENT']

config = Dynaconf(
    envvar_prefix="MP",
    core_loaders=['json'],
    default_env="development",
    environments=True,
    env_switcher="MP_ENVIRONMENT",
    settings_files=['config.json', '.secrets.json']
)

redis_config = config.redis

mysql_config = MySqlConfig(
    host=config.db.host,
    port=config.db.port,
    username=config.db.username,
    password=config.db.password,
    schema=config.db.schema,
    debug=config.db.debug.lower() == "True".lower()
)

iex_config = {
    'env': config.iex.env,
    'secret': config.iex.secret
}

# define a plaid oauth client config
plaid_config = config.plaid

mailgun_config = MailGunConfig(
    domain=config.mailgun.domain,
    api_key=config.mailgun.api_key
)
