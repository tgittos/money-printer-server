from functools import wraps
from flask import request, Response
from jwt import DecodeError

from core.repositories.profile_repository import get_repository as get_profile_repository
from core.apis.mailgun import MailGunConfig
from core.lib.logger import get_logger
from server.config import mysql_config, mailgun_config


logger = get_logger(__name__)


def authed(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        # apparently I should be using a different header for the jwt token?
        # maybe look into the jwt spec, and jwt-extended

        token = request.headers.get('Authorization')

        try:
            # token = request.authorization
            if token is not None:
                parts = token.split(' ')
                token = parts[len(parts)-1]
            else:
                return Response({
                    "success": False
                }, status=401, mimetype='application/json')

            repo = get_profile_repository(mysql_config=mysql_config, mailgun_config=mailgun_config)

            if token is not None:
                if repo.is_token_valid(token):
                    return func(*args, **kwargs)
            return Response({
                "success": False
            }, status=401, mimetype='application/json')
        except DecodeError:
            logger.exception("auth decorator received bad token from request: {0}", token)
            return Response({
                "success": False
            }, status=401, mimetype='application/json')
    return decorated


def get_identity():
    token = request.headers.get('Authorization')
    if token is not None:
        parts = token.split(' ')
        token = parts[len(parts) - 1]
    repo = get_profile_repository(mysql_config=mysql_config, mailgun_config=mailgun_config)
    profile_dict = repo.decode_jwt(token)['profile']
    return profile_dict
