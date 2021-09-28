from datetime import datetime

from core.models.profile import Profile
from core.models.plaid_item import PlaidItem
from core.lib.notifications import ProfileCreatedNotification, notify_profile_created
from core.lib.types import AccountList
from config import mailgun_config

from .requests import RegisterProfileRequest
from .auth import generate_temp_password, hash_password


@classmethod
def get_profile_by_id(cls, profile_id: int) -> Profile:
    """
    Gets a profile from the DB by its primary key
    """
    r = cls.db.query(Profile).where(Profile.id == profile_id).first()
    return r


@classmethod
def get_profile_by_email(cls, email: str) -> Profile:
    """
    Gets a profile from the DB by the user's email address
    """
    r = cls.db.query(Profile).filter(Profile.email == email).first()
    return r


@classmethod
def get_all_profiles(cls) -> AccountList:
    """
    Returns all the profiles in the DB
    """
    r = cls.db.query(Profile).all()
    return r


@classmethod
def create_profile(cls, request: RegisterProfileRequest) -> Profile:
    """
    Registers a new profile and emails the temporary password to the user
    """
    new_pw = generate_temp_password()

    new_profile = Profile()
    new_profile.email = request.email
    new_profile.password = hash_password(new_pw)
    new_profile.first_name = request.first_name
    new_profile.last_name = request.last_name
    new_profile.timestamp = datetime.utcnow()

    cls.db.add(new_profile)
    cls.db.commit()

    notify_profile_created(mailgun_config, ProfileCreatedNotification(
        profile=new_profile,
        password=new_pw
    ))

    return new_profile
