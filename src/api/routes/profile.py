from copy import Error
from flask import Blueprint, abort, request
from marshmallow import ValidationError

from core.repositories.account_repository import AccountRepository
from core.repositories.profile_repository import ProfileRepository
from core.schemas.read_schemas import ReadProfileSchema
from core.schemas.update_schemas import UpdateProfileSchema

from .decorators import authed, get_identity


profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/v1/api/profile', methods=['GET'])
@authed
def get_profile():
    user = get_identity()
    return ReadProfileSchema().dump(user)


@profile_bp.route('/v1/api/profile', methods=['PUT'])
@authed
def update_profile():
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
def sync_profile():
    user = get_identity()
    profile_repo = ProfileRepository()
    profile_repo.schedule_profile_sync(profile_id=user["id"])
    return '', 204
