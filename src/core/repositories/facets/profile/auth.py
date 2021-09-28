import bcrypt
import secrets
from datetime import datetime
from dateutil.relativedelta import relativedelta
import string
import jwt
from typing import Optional

from core.models.profile import Profile
from core.models.reset_token import ResetToken
from core.lib.notifications import ProfileCreatedNotification, PasswordResetNotification, notify_password_reset
from core.lib.types import RepositoryResponse
from config import config, mailgun_config

from .crud import create_profile, get_by_email
from .requests import ResetProfilePasswordRequest, RegisterProfileRequest, LoginRequest
from .responses import AuthResponse


@classmethod
def get_unauthenticated_user(cls) -> AuthResponse:
    """
    Gets the demo profile encoded as a token so the frontend thinks it's "authed"
    """
    demo_profile = cls.db.query(Profile).where(Profile.is_demo_profile).first()
    # TODO - maybe delete this
    if demo_profile is None:
        demo_profile = Profile()
        demo_profile.timestamp = datetime.utcnow()
        demo_profile.first_name = "Anonymous"
        demo_profile.last_name = "Money-Printer"
    jwt_token = cls.__encode_jwt(demo_profile)
    return AuthResponse(
        profile=demo_profile.to_dict(),
        token=jwt_token
    )


@classmethod
def register(cls, request: RegisterProfileRequest) -> RepositoryResponse:
    """
    Registers a user with MoneyPrinter if a user with that email doesnt
    already exist
    """
    # first, check if the request email is already taken
    existing_profile = cls.get_by_email(request.email)
    if existing_profile is not None:
        return RepositoryResponse(
            success=False,
            message="That email is not available"
        )
    new_user = create_profile(cls, request)
    return RepositoryResponse(
        success=new_user is not None,
        data=new_user
    )


@classmethod
def login(cls, request: LoginRequest) -> Optional[AuthResponse]:
    """
    Performs an authentication of the given user credentials
    Returns None of the credentials couldn't be authenticated
    """
    profile = get_by_email(request.email)
    if profile is not None:
        if check_password(profile.password, request.password):
            jwt_token = encode_jwt(profile)
            return AuthResponse(
                profile=profile.to_dict(),
                token=jwt_token
            )
    return None


@classmethod
def reset_password(cls, email: str) -> bool:
    """
    Starts the reset password flow by creating a reset token for a user
    """
    profile = get_by_email(cls, email)
    if profile is not None:
        create_reset_token(cls, profile)
        return True
    return False


@classmethod
def continue_reset_password(cls, request: ResetProfilePasswordRequest):
    """
    Continues the user-initiated password reset flow
    """
    profile = request.profile
    token = request.token
    token_entry = get_reset_token(cls, token)
    if token_entry is not None and token_entry.expiry > datetime.utcnow():
        profile.password = hash_password(request.password)
        cls.db.add(token_entry)
        cls.db.commit()
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


@classmethod
def logout(cls, email: str):
    """
    Logs a user out and expires their token (& all open tokens)
    """
    raise Exception("not implemented")


@classmethod
def create_reset_token(cls, profile: Profile):
    """
    Generates a ResetToken for the user and emails it to them
    """
    temp_pw = generate_temp_password()

    reset_token = ResetToken()
    reset_token.profile_id = profile.id
    reset_token.token = temp_pw
    reset_token.timestamp = datetime.utcnow()
    reset_token.expiry = datetime.utcnow() + relativedelta(days=1)

    cls.db.add(reset_token)
    cls.db.commit()

    notify_password_reset(mailgun_config, PasswordResetNotification(
        profile=profile,
        token=reset_token
    ))


@classmethod
def get_reset_token(cls, token_string: str) -> ResetToken:
    """
    Gets a ResetToken from the DB by the unique code sent to the user
    """
    r = cls.db.query(ResetToken).filter(ResetToken.token == token_string).first()
    return r


@staticmethod
def is_token_valid(token):
    decoded = decode_jwt(token)
    """
    Returns a boolean to indicate if the given JWT token is valid
    aside from cryptographic validity
    """
    return datetime.fromtimestamp(decoded['exp']) > datetime.utcnow()


@staticmethod
def hash_password(pt_password: str) -> bytes:
    """
    One-way hash a password using Bcrypt
    """
    return bcrypt.hashpw(pt_password.encode('utf8'), bcrypt.gensalt())


@staticmethod
def check_password(pw_hash: str, candidate: str) -> bool:
    """
    Validate a supplied plain-text against an encrypted password
    """
    return bcrypt.checkpw(candidate.encode('utf8'), pw_hash.encode('utf8'))


@staticmethod
def generate_temp_password(l: int = 16) -> str:
    """
    Generate a strong temporary password of a given length
    Defaults to 16 characters
    """
    alphabet = string.ascii_letters + string.digits + '!@#$%^&*()_+=-'
    while True:
        password = ''.join(secrets.choice(alphabet) for i in range(l))
        if (sum(c.islower() for c in password) >= 1
                and sum(c.isupper() for c in password) >= 1
                and sum(c.isdigit() for c in password) >= 1):
            break
    return password


@staticmethod
def encode_jwt(profile: Profile) -> str:
    """
    Encodes a Profile into a valid and secure JWT token
    """
    token = jwt.encode({
        "profile": profile.to_dict(),
        "authenticated": True,
        "exp": (datetime.utcnow() + relativedelta(months=1)).timestamp(),
        "algorithm": "HS256"
    }, config.secret)
    return token


@staticmethod
def decode_jwt(token: str) -> dict:
    """
    Decodes a JWT token into a dict
    """
    raw = jwt.decode(token, config.secret, algorithms=["HS256"])
    return raw
