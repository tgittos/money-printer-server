import pytest

from core.models.profile import Profile
from core.lib.actions.profile.crud import register, create_profile
from core.lib.actions.profile.requests import RegisterProfileRequest
# following import is required for spying and ensuring methods were called
import core.lib.actions.profile.crud as crud

from tests.helpers import db
from tests.factories import create_user_profile


@pytest.fixture(autouse=True)
def mock_notifier(mocker):
    mocker.patch('core.lib.actions.profile.crud.notify_profile_created')


@pytest.fixture()
def valid_register_request():
    return RegisterProfileRequest(
        email="tgittos@moneyprintergoesbrr.io",
        first_name="Tim",
        last_name="Gittos"
    )


@pytest.fixture()
def invalid_register_request():
    return RegisterProfileRequest(
        email="foooooooo.com",
        first_name=None,
        last_name=""
    )


def test_register_fails_on_used_email(db, valid_register_request):
    session = db.get_session()
    original_profile = create_user_profile(
        session, email="tgittos@moneyprintergoesbrr.io")
    assert original_profile.id is not None
    result = register(db, valid_register_request)
    assert not result.success
    #with pytest.raises(Exception):
    #    register(db, valid_register_request)
    session.close()


def test_register_creates_a_new_profile_with_valid_data(db, valid_register_request):
    result = register(db, valid_register_request)
    assert result is not None
    assert result.success
    assert result.data.id is not None
    assert result.data.email == valid_register_request.email


def test_register_fails_with_invalid_data(db, invalid_register_request):
    result = create_profile(db, invalid_register_request)
    assert not result.success


def test_create_profile_creates_profile_record(db, valid_register_request):
    result = create_profile(db, valid_register_request)
    assert result.success
    assert result.data is not None
    session = db.get_session()
    assert session.query(Profile).filter(Profile.id == result.data.id).count() == 1
    session.close()


def test_create_profile_emails_temp_password(db, valid_register_request, mocker):
    spy = mocker.spy(crud, 'notify_profile_created')
    # mocker.patch('core.lib.actions.profile.crud.notify_profile_created')
    create_profile(db, valid_register_request)
    spy.assert_called_once()


def test_create_profile_returns_profile(db, valid_register_request):
    result = create_profile(db, valid_register_request)
    assert result.success
    assert result.data.id is not None
    assert result.data.email == valid_register_request.email


def test_create_profile_fails_with_invalid_data(db, invalid_register_request):
    result = create_profile(db, invalid_register_request)
    assert not result.success
