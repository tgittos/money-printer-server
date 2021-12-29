from flask import Blueprint, request, Response, abort
from marshmallow import ValidationError

from core.schemas.scheduler_schemas import CreateScheduledJobSchema, ReadScheduledJobSchema
from core.repositories.scheduled_job_repository import ScheduledJobRepository
from .decorators import authed, admin, get_identity

from api.lib.constants import API_PREFIX

scheduler_bp = Blueprint('scheduler', __name__)


@scheduler_bp.route(f"/{API_PREFIX}/admin/schedules", methods=['GET'])
@authed
@admin
def list_schedules():
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
                    items: ReadScheduledJobSchema
      tags:
        - Scheduling
        - Admin
    """
    
    repo = ScheduledJobRepository()
    response = repo.get_scheduled_jobs()
    if response.success:
        return {
            'success': True,
            'data': ReadScheduledJobSchema(many=True).dump(response.data)
        }
    return {
        'success': False
    }, 400


@scheduler_bp.route(f"/{API_PREFIX}/admin/schedules", methods=['POST'])
@authed
@admin
def create_schedule():
    """
    ---
    post:
      summary: Create a new scheduled job based on the available jobs. This requires an admin profile.
      security:
        - jwt: []
      parameters:
        - in: request
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
                    items: ReadScheduledJobSchema
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
                'data': ReadScheduledJobSchema().dump(response.data)
            }, 201

        return {
            'success': False
        }, 400
    except ValidationError as error:
        return error.messages, 400


@scheduler_bp.route(f"/{API_PREFIX}/admin/schedules/<schedule_id>", methods=['PUT'])
@authed
@admin
def update_schedule(schedule_id):
    """
    ---
    put:
      summary: Update an existing scheduled job definition. This requires an admin profile.
      security:
        - jwt: []
      parameters:
        - in: request
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
                      items: ReadScheduledJobSchema
      tags:
        - Scheduling
        - Admin
    """
    try:
        schema = ReadScheduledJobSchema().load(request.json)

        repo = ScheduledJobRepository()
        response = repo.get_scheduled_job_by_id(schedule_id)

        if response.success:
            job = response.data

            job.job_name = schema.get('job_name') or job.job_name
            job.cron = schema.get('cron') or job.cron
            job.json_args = schema.get('json_args') or job.json_args
            job.active = schema.get('active') or job.active

            repo.update_scheduled_job(job)

            return {
                'success': True,
                'data': ReadScheduledJobSchema().dump(job)
            }

        return {
            'success': False
        }, 400
    except ValidationError as error:
        return error.messages, 400


@scheduler_bp.route(f"/{API_PREFIX}/admin/schedules/<schedule_id>", methods=['DELETE'])
@authed
@admin
def delete_schedule(schedule_id):
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
    if schedule_id is None:
        return {
            'success': False,
            'message': 'ID of scheduled job required'
        }, 400

    repo = ScheduledJobRepository()
    result = repo.get_scheduled_job_by_id(schedule_id)

    if result.success and result.data is not None:
        repo.delete_scheduled_job(result.data)
        return {
            'success': True
        }

    return {
        'success': False
    }, 400


@scheduler_bp.route(f"/{API_PREFIX}/admin/schedules/<schedule_id>/run", methods=['POST'])
@authed
@admin
def run_schedule():
    return {
        'success': False
    }


@scheduler_bp.route(f"/{API_PREFIX}/admin/schedules/instants", methods=['GET'])
@authed
@admin
def list_historical_instants():
    repo = ScheduledJobRepository()
    return {
        'success': False
    }
