from flask import Blueprint

from core.repositories.profile_repository import ProfileRepository
from auth.decorators import Authed, get_identity
from api.schemas import read_api_token_schema
from api.views.base import BaseApi
from flask_app import db


class ApiTokensApi(BaseApi):

    def __init__(self):
        super().__init__("/profile/api_tokens", 'api_token')

    def register_api(self, app):
        super().register_api(app, expose_delete=True)

    @Authed
    def get(self):
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
        repo = ProfileRepository(db)

        keys_result = repo.get_api_keys_by_profile_id(user['id'])
        if not keys_result.success or keys_result is None:
            return {
                'success': False
            }, 400

        return read_api_token_schema.dump(keys_result.data)
