import os
from flask import Blueprint
from flask import request, abort
from marshmallow import ValidationError

from core.repositories.profile_repository import ProfileRepository
from .decorators import authed, get_identity
from core.schemas.auth_schemas import ReadAuthSchema, ResetPasswordSchema, RegisterProfileSchema, LoginSchema
from core.schemas.profile_schemas import ReadProfileSchema

from api.metrics.auth_metrics import *

# define the blueprint for plaid oauth
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/v1/api/auth/register', methods=['POST'])
def register():
    """
    ---
    post:
      summary: Create a new user in the database and email a temporary password to them.
      parameters:
      - in: request
        schema: RegisterProfileSchema
      responses:
        200:
          content:
            application/json:
              schema: ReadAuthSchema
      tags:
        - Auth
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
    """
    ---
    post:
      summary: Authenticate user credentials in exchange for a JWT token.
      parameters:
      - in: request
        schema: LoginSchema
      responses:
        200:
          content:
            application/json:
              schema: ReadAuthSchema
      tags:
        - Auth
    """
    try:
        schema = LoginSchema().load(request.json)
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
    """
    ---
    post:
      summary: Initiate the user password reset process by emailing a reset link to the user.
      parameters:
      - in: email
        name: email
        schema:
            type: string
      responses:
        204:
          description: Accepted
      tags:
        - Auth
    """
    email = request.json['email']
    repo = ProfileRepository()
    result = repo.reset_password(email=email)
    # return a 204 regardless of success for security reasons
    return '', 204


@auth_bp.route('/v1/api/auth/reset/continue', methods=['POST'])
def continue_reset_password():
    """
    ---
    post:
      summary: Continue the user reset process by providing a private reset token and a new password.
      parameters:
      - in: request
        schema: ResetPasswordSchema
      responses:
        204:
          description: Accepted
      tags:
        - Auth
    """
    try:
        repo = ProfileRepository()
        result = repo.continue_reset_password(
            ResetPasswordSchema().load(request.json))
        if not result.success:
            return result.message, 400
        return '', 204
    except ValidationError as error:
        return error.messages, 400
