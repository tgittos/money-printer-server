from functools import wraps
from flask import request, Response

from core.repositories.profile_repository import get_repository


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

        repo = get_repository()

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
    repo = get_repository()
    profile_dict = repo.decode_jwt(token)['profile']
    return profile_dict
