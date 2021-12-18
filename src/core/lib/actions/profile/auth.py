from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional

from core.models.profile import Profile
from core.models.reset_token import ResetToken
from core.lib.jwt import encode_jwt, hash_password, check_password, generate_temp_password
from core.lib.notifications import PasswordResetNotification, notify_password_reset
from core.lib.types import RepositoryResponse
from config import mailgun_config
from core.lib.actions.action_response import ActionResponse

from .requests import ResetProfilePasswordRequest, LoginRequest
from .responses import AuthResponse
from .crud import get_profile_by_email


def get_unauthenticated_user(db) -> ActionResponse:
    """
    Gets the demo profile encoded as a token so the frontend thinks it's "authed"
    """
    demo_profile = db.with_session(lambda session: session.query(Profile).where(Profile.is_demo_profile).first())
    # TODO - maybe delete this
    if demo_profile is None:
        demo_profile = Profile()
        demo_profile.timestamp = datetime.utcnow()
        demo_profile.first_name = "Anonymous"
        demo_profile.last_name = "Money-Printer"
    jwt_token = encode_jwt(demo_profile)
    return ActionResponse(
        success=True,
        data= AuthResponse(
            profile=demo_profile.to_dict(),
            token=jwt_token
        )
    )


def login(cls, request: LoginRequest) -> ActionResponse:
    """
    Performs an authentication of the given user credentials
    """
    profile = get_profile_by_email(cls, request.email)
    if profile is not None:
        if check_password(profile.password, request.password):
            jwt_token = encode_jwt(profile)
            return ActionResponse(
                success=True,
                data=AuthResponse(
                    profile=profile.to_dict(),
                    token=jwt_token
                )
            )
    return ActionResponse(
        success=False,
        message=f"Login failed for ${request.email}"
    )


def reset_password(cls, email: str) -> ActionResponse:
    """
    Starts the reset password flow by creating a reset token for a user
    """
    profile = get_profile_by_email(cls, email)
    if profile is not None:
        token = create_reset_token(cls, profile)
        result = email_reset_token(cls, token)
        if result.success:
            return ActionResponse(success=True)
        return ActionResponse(
            success=False,
            message='Failure response when notifying user of password reset'
        )
    return ActionResponse(success=False)


def continue_reset_password(db, request: ResetProfilePasswordRequest) -> ActionResponse:
    """
    Continues the user-initiated password reset flow
    """
    profile = request.profile
    token = request.token
    token_entry = get_reset_token(db, token)
    if token_entry is not None and token_entry.expiry > datetime.utcnow():
        profile.password = hash_password(request.password)

        session = db.get_session()
        session.add(token_entry)
        db.commit_session(session)

        return ActionResponse(success=True)
    if token_entry is not None and token_entry.expiry < datetime.utcnow():
        return ActionResponse(
            success=False,
            message="Password reset token has expired"
        )
    return ActionResponse(success=False)


def logout(db, email: str):
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

    session = db.get_session()
    session.add(reset_token)
    db.commit_session(session)

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


def get_reset_token(db, token_string: str) -> ResetToken:
    """
    Gets a ResetToken from the DB by the unique code sent to the user
    """
    session = db.get_session()
    r = session.query(ResetToken).filter(ResetToken.token == token_string).first()
    session.close()
    return r
