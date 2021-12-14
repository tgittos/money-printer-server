from functools import wraps

import pkg_resources
from flask import request, Response, g
from jwt import DecodeError

from core.lib.jwt import is_token_valid, decode_jwt

from core.lib.logger import get_logger


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

            if token is not None:
                if is_token_valid(token):
                    g.profile = decode_jwt(token)['profile']
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


def admin(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        # this needs to be invoked after `authed` to get g.profile
        try:
            if not g.profile.is_admin:
                return Response({
                    "success": False
                }, status=401, mimetype='application/json')
            return func(*args, **kwargs)
        except Exception as ex:
            logger.exception("admin decorator received some kind of exception: {0}", ex)
            return Response({
                "success": False
            }, status=401, mimetype='application/json')
    return decorated


def get_identity():
    token = request.headers.get('Authorization')
    if token is not None:
        parts = token.split(' ')
        token = parts[len(parts) - 1]
    profile_dict = decode_jwt(token)['profile']
    return profile_dict
