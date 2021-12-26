import pytest

from core.schemas.profile_schemas import UpdateProfileSchema

from tests.fixtures.core import db
from tests.factories import create_user_profile


@pytest.fixture
def existing_profile(db):
    with db.get_session() as session:
        return create_user_profile(session)


@pytest.fixture()
def profile_with_no_plaids(db):
    with db.get_session() as session:
        return create_user_profile(session)


@pytest.fixture()
def valid_update_request(db):
    with db.get_session() as session:
        profile = create_user_profile(session)
    return UpdateProfileSchema().load({
        'id': profile.id,
        'first_name': 'New Firstname',
        'last_name': 'New Lastname'
    })


@pytest.fixture
def valid_profile_update_api_request():
    return {
        'first_name': 'New First',
        'last_name': 'New Last'
    }


@pytest.fixture
def invalid_profile_update_api_request():
    return {
        'email': 'my_new_email@example.com'
    }
