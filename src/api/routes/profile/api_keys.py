from flask import Blueprint

from core.repositories.profile_repository import ProfileRepository
from core.schemas.api_schemas import ReadApiKeySchema

from api.routes.decorators import authed, get_identity
from api.lib.constants import API_PREFIX

profile_bp = Blueprint('profile_api_keys', __name__)

@profile_bp.route(f"/{API_PREFIX}/profile/api_keys", methods=['GET'])
@authed
def get_profile_api_keys():
    """
    ---
    get:
      summary: Returns the API keys issued to the authed profile
      security:
        - jwt: []
      responses:
        200:
          content:
            application/json:
              schema: ReadApiKeySchema
      tags:
        - API Keys
    """

    user = get_identity()
    repo = ProfileRepository()

    keys_result = repo.get_api_keys_by_profile_id(user['id'])
    if not keys_result.success or keys_result is None:
        return {
            'success': False
        }, 400
    
    return ReadApiKeySchema(many=True).dump(keys_result.data)