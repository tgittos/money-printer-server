from functools import wraps
from flask import request, Response

from core.repositories.profile_repository import get_repository as get_profile_repository
from core.apis.mailgun import MailGunConfig

from server.config import config as server_config
from server.services.api import load_config
app_config = load_config()

mysql_config = app_config['db']

mailgun_config = MailGunConfig(
    api_key=server_config['mailgun']['api_key'],
    domain=server_config['mailgun']['domain']
)


def authed(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        # apparently I should be using a different header for the jwt token?
        # maybe look into the jwt spec, and jwt-extended

        # token = request.authorization
        token = request.headers.get('Authorization')
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
    return decorated


def get_identity():
    token = request.headers.get('Authorization')
    if token is not None:
        parts = token.split(' ')
        token = parts[len(parts) - 1]
    repo = get_profile_repository(mysql_config=mysql_config, mailgun_config=mailgun_config)
    profile_dict = repo.decode_jwt(token)['profile']
    return profile_dict
