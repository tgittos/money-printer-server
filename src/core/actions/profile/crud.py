from datetime import datetime

from core.models.profile import Profile
from core.schemas.auth_schemas import RegisterProfileSchema
from core.schemas.profile_schemas import CreateProfileSchema, UpdateProfileSchema
from core.actions.action_response import ActionResponse
from core.lib.jwt import generate_temp_password, hash_password
from core.lib.notifications import ProfileCreatedNotification, notify_profile_created
from core.lib.utilities import is_valid_email

from config import mailgun_config


def get_profile_by_id(db, profile_id: int) -> ActionResponse:
    """
    Gets a profile from the DB by its primary key
    """
    with db.get_session() as session:
        profile = session.query(Profile).where(
            Profile.id == profile_id).first()

    return ActionResponse(
        success=profile is not None,
        data=profile,
        message=f"No profile found with ID {profile_id}" if profile is None else None
    )


def get_profile_by_email(db, email: str) -> ActionResponse:
    """
    Gets a profile from the DB by the user's email address
    """
    with db.get_session() as session:
        profile = session.query(Profile).filter(Profile.email == email).first()

    return ActionResponse(
        success=profile is not None,
        data=profile,
        message=f"No profile found with email {email}" if profile is None else None
    )


def get_all_profiles(db) -> ActionResponse:
    """
    Returns all the profiles in the DB
    """
    with db.get_session() as session:
        profiles = session.query(Profile).all()

    return ActionResponse(
        success=profiles is not None,
        data=profiles,
        message=f"No profiles found" if profiles is None else None
    )


def register(db, request: RegisterProfileSchema) -> ActionResponse:
    """
    Registers a user with MoneyPrinter if a user with that email doesnt
    already exist
    """
    # first, check if the request email is already taken
    profile_response = get_profile_by_email(db, request['email'])
    if profile_response.data is not None:
        return ActionResponse(
            success=False,
            message="That email is unavailable for registration"
        )
    return create_profile(db, request)


def create_profile(db, request: CreateProfileSchema) -> ActionResponse:
    """
    Registers a new profile and emails the temporary password to the user
    """
    new_pw = generate_temp_password()

    new_profile = Profile()

    new_profile.email = request['email']
    new_profile.first_name = request['first_name']
    new_profile.last_name = request['last_name']
    new_profile.password = hash_password(new_pw)
    new_profile.timestamp = datetime.utcnow()

    with db.get_session() as session:
        session.add(new_profile)

        notify_result = notify_profile_created(mailgun_config, ProfileCreatedNotification(
            profile=new_profile,
            password=new_pw
        ))

        if not notify_result and notify_result.status_code != 200:
            session.rollback()
            return ActionResponse(
                success=False,
                message=f"Unsuccessful response attempting to email temp password to ${new_profile.email}"
            )
        else:
            session.commit()

    return ActionResponse(
        success=True,
        data=new_profile
    )


def update_profile(db, request: UpdateProfileSchema) -> ActionResponse:
    """
    Updates an existing profile with new information.
    Does not allow the setting of the username or email
    """
    profile_response = get_profile_by_id(db, request['id'])
    profile = profile_response.data

    if profile is None:
        return ActionResponse(
            success=False,
            message=f"Could not find profile with ID {request['id']}"
        )

    with db.get_session() as session:
        session.add(profile)

        profile.first_name = request['first_name']
        profile.last_name = request['last_name']
        profile.timestamp = datetime.utcnow()

        session.commit()

    return ActionResponse(
        success=True,
        data=profile
    )


def delete_profile(db, profile_id: int) -> ActionResponse:
    """
    Deletes an existing user profile from the database.
    This will cascade and delete all attached data.
    This delete is GPDR permanent
    """
    profile_response = get_profile_by_id(db, profile_id)
    profile = profile_response.data

    if profile is None:
        return ActionResponse(
            success=False,
            message=f"Could not find profile with ID {profile_id}"
        )

    with db.get_session() as session:
        session.delete(profile)
        session.commit()

    return ActionResponse(
        success=True
    )
