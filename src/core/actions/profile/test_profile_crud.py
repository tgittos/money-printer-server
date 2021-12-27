import pytest
from marshmallow import ValidationError

from core.models.profile import Profile
from core.schemas.profile_schemas import UpdateProfileSchema
from core.schemas.auth_schemas import RegisterProfileSchema
import core.actions.profile.crud as crud
from core.actions.profile.crud import get_profile_by_id, get_profile_by_email, get_all_profiles
from core.actions.profile.crud import register, create_profile, update_profile, delete_profile

from tests.fixtures import *


@pytest.fixture(autouse=True)
def mock_notifier(mocker):
    # mocker.patch('core.lib.notifications.notify_profile_created',
    return mocker.patch.object(crud, 'notify_profile_created',
        return_value=MockResponse(
            status_code=200
        ))


def test_cannot_construct_invalid_registraction_schema():
    with pytest.raises(ValidationError):
        register(db, RegisterProfileSchema().load({
            'email': "foooooooo.com",
            'first_name': None,
            'last_name': ""
        }))


def test_register_fails_on_used_email(db, profile_factory, valid_register_request_factory):
    request = valid_register_request_factory()
    profile = profile_factory()
    request['email'] = profile.email
    result = register(db, request)
    assert not result.success


def test_register_creates_a_new_profile_with_valid_data(db, valid_register_request_factory, mock_notifier):
    request = valid_register_request_factory()
    result = register(db, request)
    assert result is not None
    assert result.success
    assert result.data.id is not None
    assert result.data.email == request['email']


def test_create_profile_creates_profile_record(db, valid_register_request_factory, mock_notifier):
    request = valid_register_request_factory()
    result = create_profile(db, request)
    assert result.success
    assert result.data is not None
    with db.get_session() as session:
        assert session.query(Profile).filter(
            Profile.id == result.data.id).count() == 1


def test_create_profile_emails_temp_password(db, valid_register_request_factory, mock_notifier):
    request = valid_register_request_factory()
    create_profile(db, request)
    mock_notifier.assert_called_once()


def test_create_profile_returns_profile(db, valid_register_request_factory, mock_notifier):
    request = valid_register_request_factory()
    result = create_profile(db, request)
    assert result.success
    assert result.data.id is not None
    assert result.data.email == request['email']


def test_update_profile_accepts_valid_request(db, profile_factory, valid_update_request_factory):
    profile = profile_factory()
    request = valid_update_request_factory(profile_id=profile.id)
    result = update_profile(db, request)
    assert result.success
    assert result.data is not None
    assert result.data.first_name == request['first_name']
    assert result.data.last_name == request['last_name']


def test_delete_profile_removes_db_entries(db, profile_factory):
    profile = profile_factory()
    with db.get_session() as session:
        old_count = session.query(Profile).where(
            Profile.id == profile.id).count()
    result = delete_profile(db, profile.id)
    assert result.success
    assert result.data is None
    with db.get_session() as session:
        new_count = session.query(Profile).where(
            Profile.id == profile.id).count()
    assert new_count == old_count - 1


def test_get_profile_by_id_returns_profile(db, profile_factory):
    profile = profile_factory()
    profile_response = get_profile_by_id(db, profile.id)
    assert profile_response.success
    assert profile_response.data is not None
    assert profile_response.data.id == profile.id
    assert profile_response.data.email == profile.email


def test_get_profile_by_id_fails_with_missing_profile(db):
    profile_response = get_profile_by_id(db, 23234)
    assert not profile_response.success
    assert profile_response.data is None


def test_get_profile_by_email_returns_profile(db, profile_factory):
    profile = profile_factory(email='my-test-email@example.org')
    profile_response = get_profile_by_email(db, profile.email)
    assert profile_response.success
    assert profile_response.data is not None
    assert profile_response.data.id == profile.id
    assert profile_response.data.email == profile.email


def test_get_profile_by_email_fails_with_missing_profile(db):
    profile_response = get_profile_by_id(db, "foo@bar.com")
    assert not profile_response.success
    assert profile_response.data is None


def test_get_all_profiles_returns_all_profiles(db, profile_factory):
    with db.get_session() as session:
        for i in range(1, 6):
            profile_factory()
        profile_count = session.query(Profile).count()
    all_result = get_all_profiles(db)
    assert all_result.success
    assert all_result.data is not None
    assert len(all_result.data) == profile_count
