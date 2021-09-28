from flask import Blueprint, abort

from core.repositories.account_repository import AccountRepository
from core.repositories.profile_repository import ProfileRepository
from .decorators import authed, get_identity


profile_bp = Blueprint('profile', __name__)


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
