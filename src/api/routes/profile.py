from copy import Error
from flask import Blueprint, abort, request
from marshmallow import ValidationError

from core.repositories.account_repository import AccountRepository
from core.repositories.profile_repository import ProfileRepository
from core.schemas.profile_schemas import ReadProfileSchema, UpdateProfileSchema

from api.metrics.profile_metrics import *

from .decorators import authed, get_identity


profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/v1/api/profile', methods=['GET'])
@authed
@PERF_GET_PROFILE.time()
def get_profile():
    """
    ---
    get:
      summary: Return the personal details of the signed in user.
      security:
        - jwt: []
      responses:
        200:
          content:
            application/json:
              schema: ReadProfileSchema
      tags:
        - Profile
    """

    user = get_identity()
    return ReadProfileSchema().dump(user)


@profile_bp.route('/v1/api/profile', methods=['PUT'])
@authed
@PERF_UPDATE_PROFILE.time()
def update_profile():
    """
    ---
    put:
      summary: Update the user details of the signed in user.
      security:
        - jwt: []
      parameters:
      - in: request
        schema: UpdateProfileSchema
      responses:
        200:
          content:
            application/json:
              schema: ReadProfileSchema
        400:
          description: Bad request
      tags:
        - Profile
    """

    user = get_identity()
    profile_repo = ProfileRepository()
    try:
        update_result = profile_repo.update_profile({
            **{'id': user['id']},
            ** UpdateProfileSchema().load(request.json)
        })
        if update_result.success:
            return ReadProfileSchema().dump(update_result.data)
        return {
            'success': False,
            'message': update_result.message
        }, 400
    except ValidationError as err:
        return {
            'success': False,
            'message': err.messages
        }, 400


@profile_bp.route('/v1/api/profile/sync', methods=['POST'])
@authed
@PERF_SYNC_PROFILE.time()
def sync_profile():
    """
    ---
    post:
      summary: Request a full account sync for all accounts belonging to the profile.
      security:
        - jwt: []
      responses:
        204:
          description: Accepted
      tags:
        - Profile
    """
    user = get_identity()
    profile_repo = ProfileRepository()
    profile_repo.schedule_profile_sync(profile_id=user["id"])
    return '', 204
