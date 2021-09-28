import jwt
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
import bcrypt
import string
import secrets

from core.models.profile import Profile
from config import config


def is_token_valid(token):
    decoded = decode_jwt(token)
    """
    Returns a boolean to indicate if the given JWT token is valid
    aside from cryptographic validity
    """
    return datetime.fromtimestamp(decoded['exp']) > datetime.utcnow()


def hash_password(pt_password: str) -> bytes:
    """
    One-way hash a password using Bcrypt
    """
    return bcrypt.hashpw(pt_password.encode('utf8'), bcrypt.gensalt())


def check_password(pw_hash: str, candidate: str) -> bool:
    """
    Validate a supplied plain-text against an encrypted password
    """
    return bcrypt.checkpw(candidate.encode('utf8'), pw_hash.encode('utf8'))


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


def decode_jwt(token: str) -> dict:
    """
    Decodes a JWT token into a dict
    """
    raw = jwt.decode(token, config.secret, algorithms=["HS256"])
    return raw
