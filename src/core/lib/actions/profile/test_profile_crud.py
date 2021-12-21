import pytest
from marshmallow import ValidationError

from core.models.profile import Profile
from core.lib.actions.profile.crud import register, create_profile, update_profile, delete_profile
from core.schemas.request_schemas import RequestRegistrationSchema
from core.schemas.update_schemas import UpdateProfileSchema
# following import is required for spying and ensuring methods were called
import core.lib.actions.profile.crud as crud
from core.lib.actions.profile.crud import get_profile_by_id, get_profile_by_email, get_all_profiles

from tests.helpers import db
from tests.factories import create_user_profile


@pytest.fixture(autouse=True)
def mock_notifier(mocker):
    mocker.patch('core.lib.actions.profile.crud.notify_profile_created')


@pytest.fixture()
def valid_register_request():
    return RequestRegistrationSchema().load({
        'email':"tgittos@moneyprintergoesbrr.io",
        'first_name':"Tim",
        'last_name':"Gittos"
    })


@pytest.fixture()
def valid_update_request(db):
    with db.get_session() as session:
        profile = create_user_profile(session)
    return UpdateProfileSchema().load({
        'id': profile.id,
        'first_name': 'New Firstname',
        'last_name': 'New Lastname'
    })


def test_cannot_construct_invalid_registraction_schema():
    with pytest.raises(ValidationError):
        register(db, RequestRegistrationSchema().load({
            'email':"foooooooo.com",
            'first_name':None,
            'last_name':""
        }))


def test_register_fails_on_used_email(db, valid_register_request):
    with db.get_session() as session:
        original_profile = create_user_profile(
            session, email="tgittos@moneyprintergoesbrr.io")
    assert original_profile.id is not None
    result = register(db, valid_register_request)
    assert not result.success


def test_register_creates_a_new_profile_with_valid_data(db, valid_register_request):
    result = register(db, valid_register_request)
    assert result is not None
    assert result.success
    assert result.data.id is not None
    assert result.data.email == valid_register_request['email']


def test_create_profile_creates_profile_record(db, valid_register_request):
    result = create_profile(db, valid_register_request)
    assert result.success
    assert result.data is not None
    with db.get_session() as session:
        assert session.query(Profile).filter(Profile.id == result.data.id).count() == 1


def test_create_profile_emails_temp_password(db, valid_register_request, mocker):
    spy = mocker.spy(crud, 'notify_profile_created')
    # mocker.patch('core.lib.actions.profile.crud.notify_profile_created')
    create_profile(db, valid_register_request)
    spy.assert_called_once()


def test_create_profile_returns_profile(db, valid_register_request):
    result = create_profile(db, valid_register_request)
    assert result.success
    assert result.data.id is not None
    assert result.data.email == valid_register_request['email']

def test_update_profile_accepts_valid_request(db, valid_update_request):
    result = update_profile (db, valid_update_request)
    assert result.success
    assert result.data is not None
    assert result.data.first_name == valid_update_request['first_name']
    assert result.data.last_name == valid_update_request['last_name']

def test_delete_profile_removes_db_entries(db):
    with db.get_session() as session:
        profile = create_user_profile(session)
        profile_count = session.query(Profile).where(Profile.id == profile.id).count()
    assert profile_count == 1
    result = delete_profile(db, profile.id)
    assert result.success
    assert result.data is None
    with db.get_session() as session:
        profile_count = session.query(Profile).where(Profile.id == profile.id).count()
    assert profile_count == 0

def test_get_profile_by_id_returns_profile(db):
    with db.get_session() as session:
        profile = create_user_profile(session)
    profile_response = get_profile_by_id(db, profile.id)
    assert profile_response.success
    assert profile_response.data is not None
    assert profile_response.data.id == profile.id
    assert profile_response.data.email == profile.email


def test_get_profile_by_id_fails_with_missing_profile(db):
    profile_response = get_profile_by_id(db, 23234)
    assert not profile_response.success
    assert profile_response.data is None


def test_get_profile_by_email_returns_profile(db):
    with db.get_session() as session:
        profile = create_user_profile(session)
    profile_response = get_profile_by_email(db, profile.email)
    assert profile_response.success
    assert profile_response.data is not None
    assert profile_response.data.id == profile.id
    assert profile_response.data.email == profile.email


def test_get_profile_by_email_fails_with_missing_profile(db):
    profile_response = get_profile_by_id(db, "foo@bar.com")
    assert not profile_response.success
    assert profile_response.data is None


def test_get_all_profiles_returns_all_profiles(db):
    with db.get_session() as session:
        for i in range(1, 6):
            create_user_profile(session, email=f"user{i}@example.com")
    all_result = get_all_profiles(db) 
    assert all_result.success
    assert all_result.data is not None
    assert len(all_result.data) == 5


def test_get_all_profiles_returns_empty_array_with_no_profiles(db):
    profile_response = get_all_profiles(db)
    assert profile_response.success
    assert len(profile_response.data) == 0
