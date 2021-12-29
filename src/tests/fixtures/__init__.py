from .account_fixtures import *
from .core import *
from .api_fixtures import *
from .notification_fixtures import *
from .scheduler_fixtures import *
from .profile_fixtures import *
from .plaid_item_fixtures import *
from .auth_fixtures import *
import pytest
import random


@pytest.fixture(scope='function', autouse=True)
def faker_seed():
    return random.randint(1, 50000)
