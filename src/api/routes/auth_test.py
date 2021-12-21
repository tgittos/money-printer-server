import pytest

from tests.factories import create_user_profile
from tests.helpers import db, client


@pytest.mark.skip(reason="need to go back and implement this")
def test_register_calls_into_profile_repository(client):
    assert False


@pytest.mark.skip(reason="need to go back and implement this")
def test_register_returns_a_valid_json(client):
    assert False
