import pytest

from tests.factories import create_user_profile
from tests.helpers import db, client


def test_register_accepts_valid_input():
    assert False


def test_register_rejects_invalid_input():
    assert False


def test_register_rejects_duplicate_email():
    assert False


def test_login_accepts_valid_credentials():
    assert False


def test_login_rejects_bad_username():
    assert False


def test_login_rejects_bad_password():
    assert False


def test_auth_tokens_are_valid_for_30_days():
    assert False


def test_reset_password_sends_token_email():
    assert False


def test_reset_password_accepts_bad_email_but_doesnt_send():
    assert False


def test_continue_reset_accepts_valid_token():
    assert False


def test_continue_reset_rejects_invalid_token():
    assert False
