import os
from dynaconf import Dynaconf

from core.apis.mailgun import MailGunConfig

env = 'development'
if 'MP_ENVIRONMENT' in os.environ:
    env = os.environ['MP_ENVIRONMENT']

config = Dynaconf(
    envvar_prefix="MP",
    core_loaders=['json'],
    default_env="development",
    environments=True,
    env_switcher="MP_ENVIRONMENT",
    settings_files=['config.json']
)

redis_config = config.redis

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
