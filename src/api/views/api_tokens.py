from flask import Blueprint

from core.repositories.profile_repository import ProfileRepository
from api.schemas import read_api_token_schema

from api.routes.decorators import authed, get_identity
from api.lib.constants import API_PREFIX
from api.views.base import BaseApi


class ApiTokenApi(BaseApi):

    def __init__(self):
        super().__init__("/profile/api_tokens", 'api_tokens')

    def register_api(self, app):
        super().register_api(app, expose_delete=True)

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
                schema: ReadApiTokenApiSchema
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

        return read_api_token_schema.dump(keys_result.data)
