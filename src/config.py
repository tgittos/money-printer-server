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