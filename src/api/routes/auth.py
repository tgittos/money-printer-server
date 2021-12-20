from flask import Blueprint
from flask import request, abort
from marshmallow import ValidationError

from core.models.profile import ProfileSchema
from core.repositories.profile_repository import ProfileRepository, RegisterProfileRequest, LoginRequest
from .decorators import authed, get_identity
from config import mysql_config, mailgun_config
from api.schemas.auth_schemas import RegisterProfileSchema, AuthSchema

# define the blueprint for plaid oauth
auth_bp = Blueprint('auth', __name__)




@auth_bp.route('/v1/api/auth/register', methods=['POST'])
def register():
    try:
        schema = RegisterProfileSchema().load(request.json)
        repo = ProfileRepository()
        result = repo.register(schema)
        return ProfileSchema().dumps(result)

    except ValidationError as error:
        return error.messages, 400
    except Exception:
        abort(500)



@auth_bp.route('/v1/api/auth/unauthenticated', methods=['GET'])
def get_unauthenticated_user():
    repo = ProfileRepository()
    result = repo.get_unauthenticated_user()
    if result is None:
        return {
            'message': 'No unauthenticated user configured'
        }, 404
    return ({
        'success': True,
        'data': result
    })


@auth_bp.route('/v1/api/auth/login', methods=['POST'])
def login():
    try:
        schema = AuthSchema().load(request.json)
        repo = ProfileRepository()
        result = repo.login(schema)

        if result is None:
            return {
                'success': False,
                'message': 'Username/password combination not found'
            }, 404

        return {
            'success': True,
            'data': result
        }
    except ValidationError as error:
        return error.messages, 400
    except Exception:
        abort(500)


@auth_bp.route('/v1/api/auth/logout', methods=['POST'])
@authed
def logout():
    username = request.json['username']
    repo = ProfileRepository()
    result_json = repo.logout(username=username)

    return result_json


@auth_bp.route('/v1/api/auth/reset', methods=['POST'])
def reset_password():
    user = get_identity()
    repo = ProfileRepository()
    result_json = repo.reset_password(username=user['username'])
    return result_json


@auth_bp.route('/v1/api/auth/reset/continue', methods=['POST'])
def continue_reset_password():
    user = get_identity()
    token = request.json['token']
    new_password = request.json['password']
    repo = ProfileRepository()
    result = repo.continue_reset_password(username=user['username'], token=token, password=new_password)
    return result

