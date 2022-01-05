from functools import partial

from flask import request, Response, g
from jwt import DecodeError

from core.lib.jwt import is_token_valid, decode_jwt

from core.lib.logger import get_logger


logger = get_logger(__name__)


def decode_token():
    # apparently I should be using a different header for the jwt token?
    # maybe look into the jwt spec, and jwt-extended
    try:
        if 'Authorization' in request.headers:
            token = request.headers.get('Authorization')
            if token is not None:
                parts = token.split(' ')
                token = parts[len(parts) - 1]
            if is_token_valid(token):
                return decode_jwt(token)
    except DecodeError:
        logger.exception(
            "auth decorator received bad token from request: {0}", token)
        return Response({
            "success": False
        }, status=400, mimetype='application/json')


def get_identity():
    token = decode_token()
    if token is not None:
        return decode_token()['profile']
    return None


class authed:
    def __init__(self, func):
        self.func = func
 
    def __get__(self, instance, owner):
        p = partial(self.__call__, instance)
        p.__name__ = str(self.func)
        return p
    
    def __call__(self, *args, **kwargs):
        token = decode_token()
        if token is None:
            return Response({
                "success": False
            }, status=401, mimetype='application/json')

        # if we were unable to get a token from the decode,
        # and we hit this point, then we're not authed
        profile = token['profile']
        if profile is None:
            return Response({
                "success": False
            }, status=401, mimetype='application/json')

        return self.func(*args, **kwargs)
   


class admin:
    def __init__(self, func):
        self.func = func
    
    def __get__(self, instance, owner):
        p = partial(self.__call__, instance)
        p.__name__ = str(self.func)
        return p

    def __call__(self, *args, **kwargs):
        token = decode_token()
        if not token or not token['is_admin']:
            return Response({
                "success": False
            }, status=401, mimetype='application/json')
        return self.func(*args, **kwargs)

