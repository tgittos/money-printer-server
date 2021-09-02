from functools import wraps
from flask import request, Response

from core.repositories.profile_repository import get_repository


def authed(func):
    @wraps(func)
    def decorated(*args, **kwargs):
        token = request.authorization
        repo = get_repository()
        if token is not None:
            if repo.is_token_valid(token):
                return func(*args, **kwargs)
        return Response({
            "success": False
        }, status=401, mimetype='application/json')
    return decorated
