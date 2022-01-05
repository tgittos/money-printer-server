from flask import Blueprint, request, Response, abort
from marshmallow import ValidationError

from core.schemas import CreateScheduledJobSchema
from core.repositories.scheduled_job_repository import ScheduledJobRepository

from api.schemas import read_scheduled_jobs_schema, read_scheduled_job_schema
from api.lib.constants import API_PREFIX
from api.views.base import BaseApi

from api.views.decorators import authed, admin, get_identity


class SchedulerApi(BaseApi):

    def __init__(self):
        super().__init__("/admin/schedules", 'schedules')

    def register_api(self, app):
        super().register_api(app, expose_delete=True)
        self.add_url(app, "/<id>/run", self.run_schedule, methods=['POST'])
        self.add_url(app, '/instants', self.list_historical_instants)


    @authed
    @admin
    def get(self):
        """
        ---
        get:
            summary: List the currently active scheduled jobs. This requires an admin profile.
            security:
                - jwt: []
            responses:
                200:
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    success:
                                        type: boolean
                                    data:
                                        type: array
                                        items: ReadScheduledJobApiSchema
        tags:
            - Scheduling
            - Admin
        """

        repo = ScheduledJobRepository()
        response = repo.get_scheduled_jobs()
        if response.success:
            return {
                'success': True,
                'data': read_scheduled_jobs_schema.dump(response.data)
            }
        return {
            'success': False
        }, 400


    @authed
    @admin
    def post(self):
        """
        ---
        post:
            summary: Create a new scheduled job based on the available jobs. This requires an admin profile.
            security:
                - jwt: []
            requestBody:
                content:
                    application/json:
                        schema: CreateScheduledJobSchema
            responses:
                200:
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    success:
                                        type: boolean
                                    data:
                                        type: array
                                        items: ReadScheduledJobApiSchema
        tags:
            - Scheduling
            - Admin
        """
        try:
            repo = ScheduledJobRepository()
            schema = CreateScheduledJobSchema().load(request.json)
            response = repo.create_scheduled_job(schema)

            if response.success:
                return {
                    'success': True,
                    'data': read_scheduled_jobs_schema.dump(response.data)
                }, 201

            return {
                'success': False
            }, 400
        except ValidationError as error:
            return error.messages, 400


    @authed
    @admin
    def put(self, id):
        """
        ---
        put:
            summary: Update an existing scheduled job definition. This requires an admin profile.
            security:
                - jwt: []
            requestBody:
                content:
                    application/json:
                        schema: UpdateScheduledJobSchema
            responses:
                200:
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    success:
                                        type: boolean
                                    data:
                                        type: array
                                        items: ReadScheduledJobApiSchema
        tags:
            - Scheduling
            - Admin
        """
        try:
            schema = read_scheduled_job_schema.load(request.json)

            repo = ScheduledJobRepository()
            response = repo.get_scheduled_job_by_id(id)

            if response.success:
                job = response.data

                job.job_name = schema.get('job_name') or job.job_name
                job.cron = schema.get('cron') or job.cron
                job.json_args = schema.get('json_args') or job.json_args
                job.active = schema.get('active') or job.active

                repo.update_scheduled_job(job)

                return {
                    'success': True,
                    'data': read_scheduled_job_schema.dump(job)
                }

            return {
                'success': False
            }, 400
        except ValidationError as error:
            return error.messages, 400


    @authed
    @admin
    def delete(self, id):
        """
        ---
        delete:
            summary: Delete an existing scheduled job definition. This requires an admin profile.
            security:
                - jwt: []
            parameters:
                - in: schedule_id
                  name: schedule_id
                  type: Integer
            responses:
                200:
                    content:
                        application/json:
                            schema:
                                type: object
                                properties:
                                    success:
                                        type: boolean
        tags:
            - Scheduling
            - Admin
        """
        if id is None:
            return {
                'success': False,
                'message': 'ID of scheduled job required'
            }, 400

        repo = ScheduledJobRepository()
        result = repo.get_scheduled_job_by_id(id)

        if result.success and result.data is not None:
            repo.delete_scheduled_job(result.data)
            return {
                'success': True
            }

        return {
            'success': False
        }, 400


    @authed
    @admin
    def run_schedule(self):
        return {
            'success': False
        }


    @authed
    @admin
    def list_historical_instants(self):
        repo = ScheduledJobRepository()
        return {
            'success': False
        }
