import secrets
import string
import bcrypt

from core.stores.mysql import MySql
from core.models.profile import Profile
from core.lib.notifications import notify_profile_created, ProfileCreatedNotification, MailGunConfig


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

    def __init__(self, success, message = None, data = None):
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
    mailgun_config=MailGunConfig()
    mysql_config=None

    def __init__(self, mailgun_config, mysql_config):
        self.mailgun_config = mailgun_config
        self.mysql_config = mysql_config


class ProfileRepository:

    def __init__(self, profile_config):
        self.config = profile_config
        db = MySql(self.config.mysql_config)
        self.db = db.get_session()

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

    def login(self, email, password):
        raise Exception("not implemented")

    def reset_password(self, email):
        raise Exception("not implemented")

    def logout(self, email):
        raise Exception("not implemented")

    def get_by_email(self, email):
        record = self.db.query(Profile).filter(Profile.email==email).first()
        return record

    def __create_profile(self, request):
        new_pw = self.__generate_temp_password()
        new_profile = Profile()
        new_profile.email = request.email
        new_profile.password = self.__hash_password(new_pw)
        new_profile.first_name = request.first_name
        new_profile.last_name = request.last_name

        self.db.add(new_profile)
        self.db.commit()

        notify_profile_created(self.config.mailgun_config, ProfileCreatedNotification(
            profile=new_profile,
            password=new_pw
        ))

        return new_profile

    def __hash_password(self, pt_password):
        return bcrypt.hashpw(pt_password, bcrypt.gensalt())

    def __check_password(self, hash, candidate):
        return bcrypt.checkpw(candidate, hash)

    def __generate_temp_password(self, len=16):
        alphabet = string.ascii_letters + string.digits + '!@#$%^&*()_+=-'
        while True:
            password = ''.join(secrets.choice(alphabet) for i in range(len))
            if (sum(c.islower() for c in password) >= 1
                    and sum(c.isupper() for c in password) >= 1
                    and sum(c.isdigit() for c in password) >= 1):
                break
        return password
