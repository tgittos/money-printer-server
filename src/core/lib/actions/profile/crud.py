from datetime import datetime

from core.models.profile import Profile
from core.lib.jwt import generate_temp_password, hash_password
from core.lib.notifications import ProfileCreatedNotification, notify_profile_created
from core.lib.types import AccountList, RepositoryResponse
from config import mailgun_config

from .requests import RegisterProfileRequest


def get_profile_by_id(db, profile_id: int) -> Profile:
    """
    Gets a profile from the DB by its primary key
    """
    session = db.get_session()
    r = session.query(Profile).where(Profile.id == profile_id).first()
    session.close()
    return r


def get_profile_by_email(db, email: str) -> Profile:
    """
    Gets a profile from the DB by the user's email address
    """
    session = db.get_session()
    r = session.query(Profile).filter(Profile.email == email).first()
    session.close()
    return r


def get_all_profiles(db) -> AccountList:
    """
    Returns all the profiles in the DB
    """
    session = db.get_session()
    r = session.query(Profile).all()
    session.close()
    return r


def create_profile(db, request: RegisterProfileRequest) -> Profile:
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

    session = db.get_session()
    session.add(new_profile)
    db.commit_session(session)

    notify_profile_created(mailgun_config, ProfileCreatedNotification(
        profile=new_profile,
        password=new_pw
    ))

    return new_profile


def register(db, request: RegisterProfileRequest) -> RepositoryResponse:
    """
    Registers a user with MoneyPrinter if a user with that email doesnt
    already exist
    """
    # first, check if the request email is already taken
    existing_profile = get_profile_by_email(db, request.email)
    if existing_profile is not None:
        return RepositoryResponse(
            success=False,
            message="That email is not available"
        )
    new_user = create_profile(db, request)
    return RepositoryResponse(
        success=new_user is not None,
        data=new_user
    )
