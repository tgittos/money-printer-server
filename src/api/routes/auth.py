import os
from flask import Blueprint
from flask import request, abort
from marshmallow import ValidationError

from core.repositories.profile_repository import ProfileRepository
from .decorators import authed, get_identity
from api.schemas.auth_schemas import RegisterProfileSchema, AuthSchema
from core.schemas.read_schemas import ReadProfileSchema, ReadAuthSchema
from core.schemas.request_schemas import RequestPasswordResetSchema

# define the blueprint for plaid oauth
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/v1/api/auth/register', methods=['POST'])
def register():
    """Create a new user in the database and email a temporary password to them.
    ---
    post:
      parameters:
      - in: request
        schema: RegisterProfileSchema
      responses:
        200:
          content:
            application/json:
              schema: ReadAuthSchema
    """
    try:
        schema = RegisterProfileSchema().load(request.json)
        repo = ProfileRepository()
        result = repo.register(schema)
        if result.success:
            return ReadProfileSchema().dump(result.data)
        else:
            return {
                'success': False,
                'message': result.message
            }, 400

    except ValidationError as error:
        return error.messages, 400


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
    """Authenticate user credentials in exchange for a JWT token
    ---
    post:
      parameters:
      - in: request
        schema: RequestAuthSchema
      responses:
        200:
          content:
            application/json:
              schema: ReadAuthSchema
    """
    try:
        schema = AuthSchema().load(request.json)
        repo = ProfileRepository()
        result = repo.login(schema)

        if not result.success:
            return {
                'success': False,
                'message': 'Username/password combination not found'
            }, 404

        return ReadAuthSchema().dump(result.data)

    except ValidationError as error:
        return error.messages, 400


@auth_bp.route('/v1/api/auth/reset', methods=['POST'])
def reset_password():
    """Initiate the user password reset process by emailing a reset link to the user.
    ---
    post:
      parameters:
      - in: email
        name: email
        schema:
            type: string
      responses:
        204:
          description: Accepted
    """
    email = request.json['email']
    repo = ProfileRepository()
    result = repo.reset_password(email=email)
    # return a 204 regardless of success for security reasons
    return '', 204


@auth_bp.route('/v1/api/auth/reset/continue', methods=['POST'])
def continue_reset_password():
    """Initiate the user password reset process by emailing a reset link to the user.
    ---
    post:
      parameters:
      - in: request
        schema: RequestPasswordResetSchema
      responses:
        204:
          description: Accepted
    """

    email = request.json['email']
    token = request.json['token']
    new_password = request.json['password']
    repo = ProfileRepository()
    result = repo.continue_reset_password(
        RequestPasswordResetSchema().load(request.json))
    if not result.success:
        return result.message, 400
    return '', 204
