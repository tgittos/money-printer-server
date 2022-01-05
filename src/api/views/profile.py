from copy import Error
from flask import Blueprint, abort, request
from marshmallow import ValidationError

from core.repositories.profile_repository import ProfileRepository
from core.schemas import UpdateProfileSchema
from api.schemas import read_profile_schema

from api.views.base import BaseApi
from api.lib.constants import API_PREFIX
from api.metrics.profile_metrics import *

from api.views.decorators import Authed, get_identity


class ProfileApi(BaseApi):

    def __init__(self):
        super().__init__('/profiles', 'profile')

    def register_api(self, app):
        self.add_url(app, "/", self.get)
        self.add_url(app, "/", self.update, methods=['PUT'])
        self.add_url(app, "/sync", self.sync_profile, methods=['POST'])


    @Authed
    @PERF_GET_PROFILE.time()
    def get(self):
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
                            schema: ReadProfileApiSchema
            tags:
                - Profile
        """

        user = get_identity()
        return read_profile_schema.dump(user)


    @Authed
    @PERF_UPDATE_PROFILE.time()
    def update(self):
        """
        ---
        put:
            summary: Update the user details of the signed in user.
            security:
                - jwt: []
            requestBody:
                content:
                    application/json:
                        schema: UpdateProfileSchema
            responses:
                200:
                    content:
                        application/json:
                            schema: ReadProfileApiSchema
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
                return read_profile_schema.dump(update_result.data)
            return {
                'success': False,
                'message': update_result.message
            }, 400
        except ValidationError as err:
            return {
                'success': False,
                'message': err.messages
            }, 400


    @Authed
    @PERF_SYNC_PROFILE.time()
    def sync_profile(self):
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
