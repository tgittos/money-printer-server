from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional

from core.models.profile import Profile
from core.models.reset_token import ResetToken
from core.lib.jwt import encode_jwt, hash_password, check_password, generate_temp_password
from core.lib.notifications import PasswordResetNotification, notify_password_reset
from config import mailgun_config
from core.lib.actions.action_response import ActionResponse
from core.schemas.read_schemas import ReadAuthSchema, ReadProfileSchema
from core.schemas.request_schemas import RequestAuthSchema, RequestPasswordResetSchema

from .crud import get_profile_by_email


def get_unauthenticated_user(db) -> ActionResponse:
    """
    Gets the demo profile encoded as a token so the frontend thinks it's "authed"
    """
    with db.get_session() as session:
        demo_profile = session.query(Profile).where(
            Profile.is_demo_profile).first()
        # TODO - maybe delete this
        if demo_profile is None:
            demo_profile = Profile()
            demo_profile.timestamp = datetime.utcnow()
            demo_profile.first_name = "Anonymous"
            demo_profile.last_name = "Money-Printer"
        jwt_token = encode_jwt(demo_profile)
        return ActionResponse(
            success=True,
            data=[demo_profile, jwt_token]
        )


def login(db, request: RequestAuthSchema) -> ActionResponse:
    """
    Performs an authentication of the given user credentials
    """
    profile_result = get_profile_by_email(db, request['email'])
    profile = profile_result.data

    if not profile_result.success:
        return ActionResponse(
            success=False,
            message=f"Login failed for ${request['email']}"
        )

    if check_password(profile.password, request['password']):
        jwt_token = encode_jwt(profile)

        return ActionResponse(
            success=True,
            data=[profile, jwt_token]
        )

    return ActionResponse(
        success=False,
        message=f"Login failed for ${request['email']}"
    )


def reset_password(db, email: str) -> ActionResponse:
    """
    Starts the reset password flow by creating a reset token for a user
    """
    response = get_profile_by_email(db, email)
    if response.success:
        token_result = create_reset_token(db, response.data)
        if token_result.success:
            email_result = email_reset_token(db, token_result.data)
        if email_result and email_result.success:
            return ActionResponse(success=True)
        return ActionResponse(
            success=False,
            message='Failure response when notifying user of password reset'
        )
    return ActionResponse(success=False)


def continue_reset_password(db, request: RequestPasswordResetSchema) -> ActionResponse:
    """
    Continues the user-initiated password reset flow
    """
    profile = request['profile']
    token = request['token']

    token_entry = get_reset_token(db, token)

    if token_entry is not None and token_entry.expiry > datetime.utcnow():
        profile.password = hash_password(request['password'])

        with db.get_session() as session:
            session.add(token_entry)
            session.commit()

        return ActionResponse(success=True)

    if token_entry is not None and token_entry.expiry < datetime.utcnow():
        return ActionResponse(
            success=False,
            message="Password reset token has expired"
        )

    return ActionResponse(success=False)


def logout(db, email: str) -> ActionResponse:
    """
    Logs a user out and expires their token (& all open tokens)
    """
    raise Exception("not implemented")


def create_reset_token(db, profile: Profile) -> ActionResponse:
    """
    Generates a ResetToken for the user and emails it to them
    """
    temp_pw = generate_temp_password()

    reset_token = ResetToken()
    reset_token.profile_id = profile.id
    reset_token.token = temp_pw
    reset_token.timestamp = datetime.utcnow()
    reset_token.expiry = datetime.utcnow() + relativedelta(days=1)

    with db.get_session() as session:
        session.add(reset_token)
        session.commit()

    return ActionResponse(
        success=True,
        data=reset_token
    )


def email_reset_token(profile, reset_token) -> ActionResponse:
    """
    Emails the reset password flow start notification to the user
    """
    result = notify_password_reset(mailgun_config, PasswordResetNotification(
        profile=profile,
        token=reset_token
    ))
    return ActionResponse(
        success=result.status_code == 200
    )


def get_reset_token(db, token_string: str) -> ActionResponse:
    """
    Gets a ResetToken from the DB by the unique code sent to the user
    """
    with db.get_session() as session:
        r = session.query(ResetToken).filter(
            ResetToken.token == token_string).first()
    return r
