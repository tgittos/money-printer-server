from copy import Error
from flask import Blueprint, abort

from core.repositories.account_repository import AccountRepository
from core.repositories.profile_repository import ProfileRepository
from .decorators import authed, get_identity


profile_bp = Blueprint('profile', __name__)


@profile_bp.route('/v1/api/profile', methods=['GET'])
@authed
def get_profile():
    raise Error("oops, not done")


@profile_bp.route('/v1/api/profile', methods=['PUT'])
@authed
def update_profile():
    raise Error("oops, not done")


@profile_bp.route('/v1/api/profile/sync', methods=['POST'])
@authed
def sync_profile():
    user = get_identity()
    profile_repo = ProfileRepository()
    profile = profile_repo.get_profile_by_id(user["id"])
    profile_repo.schedule_profile_sync(profile=profile)
    return {
        'success': True
    }
