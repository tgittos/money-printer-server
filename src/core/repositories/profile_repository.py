import secrets
import string
import bcrypt
from datetime import datetime
from dateutil.relativedelta import relativedelta
import jwt

from core.stores.mysql import MySql
from core.models.profile import Profile
from core.models.reset_token import ResetToken
from core.lib.notifications import notify_profile_created, ProfileCreatedNotification, MailGunConfig,\
    PasswordResetNotification, notify_password_reset
from config import config


def get_repository(mysql_config, mailgun_config):
    repo = ProfileRepository(ProfileRepositoryConfig(
        mailgun_config=mailgun_config,
        mysql_config=mysql_config
    ))
    return repo


class ProfileExistsException(Exception):
    email = None

    def __init__(self, _email):
        self.__init__()
        email = _email


class RegisterProfileRequest(object):
    email = None
    first_name = None
    last_name = None

    def __init__(self, email, first_name, last_name):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name


class RegisterProfileResponse(object):
    success = False
    message = None
    data = None

    def __init__(self, success, message=None, data=None):
        self.success = success
        self.message = message
        self.data = data


class ResetProfilePasswordRequest(object):
    profile = None
    token = None
    password = None

    def __init__(self, profile, token, password):
        self.profile = profile
        self.token = token
        self.password = password


class ResetProfilePasswordResponse(object):
    success = False
    message = None
    data = None

    def __init__(self, success, message=None, data=None):
        self.success = success
        self.message = message
        self.data = data


class LoginRequest(object):
    email = None
    password = None

    def __init__(self, email, password):
        self.email = email
        self.password = password


class ProfileRepositoryConfig(object):
    mailgun_config = MailGunConfig()
    mysql_config = None

    def __init__(self, mailgun_config, mysql_config):
        self.mailgun_config = mailgun_config
        self.mysql_config = mysql_config


class ProfileRepository:

    def __init__(self, profile_config):
        self.config = profile_config
        db = MySql(self.config.mysql_config)
        self.db = db.get_session()

    def get_unauthenticated_user(self):
        demo_profile = self.db.query(Profile).where(Profile.is_demo_profile).first()
        # TODO - maybe delete this
        if demo_profile is None:
            demo_profile = Profile()
            demo_profile.timestamp = datetime.utcnow()
            demo_profile.first_name = "Anonymous"
            demo_profile.last_name = "Money-Printer"
        jwt_token = self.__encode_jwt(demo_profile)
        return {
            "profile": demo_profile.to_dict(),
            "token": jwt_token
        }

    def register(self, request):
        # first, check if the request email is already taken
        existing_profile = self.get_by_email(request.email)
        if existing_profile is not None:
            return RegisterProfileResponse(
                success=False,
                message="That email is not available"
            )
        new_user = self.__create_profile(request)
        return RegisterProfileResponse(
            success=new_user is not None,
            data=new_user
        )

    def login(self, request):
        profile = self.get_by_email(request.email)
        if profile is not None:
            if self.__check_password(profile.password, request.password):
                jwt_token = self.__encode_jwt(profile)
                return {
                    "profile": profile.to_dict(),
                    "token": jwt_token
                }
        return None

    def reset_password(self, email):
        profile = self.get_by_email(email)
        if profile is not None:
            self.__create_reset_token(profile)
            return True
        return False

    def continue_reset_password(self, request):
        profile = request.profile
        token = request.token
        token_entry = self.__get_reset_token(token)
        if token_entry is not None and token_entry.expiry > datetime.utcnow():
            profile.password = self.__hash_password(request.password)
            self.db.add(token_entry)
            self.db.commit()
            return ResetProfilePasswordResponse(
                success=True
            )
        if token_entry is not None and token_entry.expiry < datetime.utcnow():
            return ResetProfilePasswordResponse(
                success=False,
                message="Password reset token has expired"
            )
        return ResetProfilePasswordResponse(
            success=False
        )

    def logout(self, email):
        raise Exception("not implemented")

    def get_by_email(self, email):
        record = self.db.query(Profile).filter(Profile.email==email).first()
        return record

    def get_by_id(self, id):
        record = self.db.query(Profile).filter(Profile.id==id).first()
        return record

    def is_token_valid(self, token):
        decoded = self.decode_jwt(token)
        return datetime.fromtimestamp(decoded['exp']) > datetime.utcnow()

    def get_all_profiles(self):
        records = self.db.query(Profile).all()
        return records

    def __create_profile(self, request):
        new_pw = self.__generate_temp_password()
        new_profile = Profile()
        new_profile.email = request.email
        new_profile.password = self.__hash_password(new_pw)
        new_profile.first_name = request.first_name
        new_profile.last_name = request.last_name
        new_profile.timestamp = datetime.utcnow()

        self.db.add(new_profile)
        self.db.commit()

        notify_profile_created(self.config.mailgun_config, ProfileCreatedNotification(
            profile=new_profile,
            password=new_pw
        ))

        return new_profile

    def __create_reset_token(self, profile):
        temp_pw = self.__generate_temp_password()
        reset_token = ResetToken()
        reset_token.profile_id = profile.id
        reset_token.token = temp_pw
        reset_token.timestamp = datetime.utcnow()
        reset_token.expiry = datetime.utcnow() + relativedelta(days=1)

        self.db.add(reset_token)
        self.db.commit()

        notify_password_reset(self.config.mailgun_config, PasswordResetNotification(
            profile=profile,
            token=reset_token
        ))

    def __get_reset_token(self, token_string):
        record = self.db.query(ResetToken).filter(ResetToken.token==token_string).first()
        return record

    def __hash_password(self, pt_password):
        return bcrypt.hashpw(pt_password.encode('utf8'), bcrypt.gensalt())

    def __check_password(self, pw_hash, candidate):
        return bcrypt.checkpw(candidate.encode('utf8'), pw_hash)

    def __generate_temp_password(self, len=16):
        alphabet = string.ascii_letters + string.digits + '!@#$%^&*()_+=-'
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(len))
            if (sum(c.islower() for c in password) >= 1
                    and sum(c.isupper() for c in password) >= 1
                    and sum(c.isdigit() for c in password) >= 1):
                break
        return password

    def __encode_jwt(self, profile):
        token = jwt.encode({
            "profile": profile.to_dict(),
            "authenticated": True,
            "exp": (datetime.utcnow() + relativedelta(months=1)).timestamp(),
            "algorithm": "HS256"
        }, config.secret)
        return token

    def decode_jwt(self, token):
        raw = jwt.decode(token, config.secret, algorithms=["HS256"])
        return raw
