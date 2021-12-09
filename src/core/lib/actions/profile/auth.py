from datetime import datetime
from dateutil.relativedelta import relativedelta
from typing import Optional

from core.models.profile import Profile
from core.models.reset_token import ResetToken
from core.lib.jwt import encode_jwt, hash_password, check_password, generate_temp_password
from core.lib.notifications import PasswordResetNotification, notify_password_reset
from core.lib.types import RepositoryResponse
from config import mailgun_config

from .requests import ResetProfilePasswordRequest, LoginRequest
from .responses import AuthResponse
from .crud import get_profile_by_email


def get_unauthenticated_user(db) -> AuthResponse:
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
    return AuthResponse(
        profile=demo_profile.to_dict(),
        token=jwt_token
    )


def login(cls, request: LoginRequest) -> Optional[AuthResponse]:
    """
    Performs an authentication of the given user credentials
    Returns None of the credentials couldn't be authenticated
    """
    profile = get_profile_by_email(cls, request.email)
    if profile is not None:
        if check_password(profile.password, request.password):
            jwt_token = encode_jwt(profile)
            return AuthResponse(
                profile=profile.to_dict(),
                token=jwt_token
            )
    return None


def reset_password(cls, email: str) -> bool:
    """
    Starts the reset password flow by creating a reset token for a user
    """
    profile = get_profile_by_email(cls, email)
    if profile is not None:
        create_reset_token(cls, profile)
        return True
    return False


def continue_reset_password(db, request: ResetProfilePasswordRequest):
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

        return RepositoryResponse(
            success=True
        )
    if token_entry is not None and token_entry.expiry < datetime.utcnow():
        return RepositoryResponse(
            success=False,
            message="Password reset token has expired"
        )
    return RepositoryResponse(
        success=False
    )


def logout(db, email: str):
    """
    Logs a user out and expires their token (& all open tokens)
    """
    raise Exception("not implemented")


def create_reset_token(db, profile: Profile):
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

    notify_password_reset(mailgun_config, PasswordResetNotification(
        profile=profile,
        token=reset_token
    ))


def get_reset_token(db, token_string: str) -> ResetToken:
    """
    Gets a ResetToken from the DB by the unique code sent to the user
    """
    session = db.get_session()
    r = session.query(ResetToken).filter(ResetToken.token == token_string).first()
    session.close()
    return r
