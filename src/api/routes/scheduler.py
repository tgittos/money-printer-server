from flask import Blueprint, request, Response, abort
from marshmallow import ValidationError

from core.schemas.read_schemas import ReadScheduledJobSchema
from core.schemas.create_schemas import CreateScheduledJobSchema
from core.repositories.scheduled_job_repository import ScheduledJobRepository
from .decorators import authed, admin, get_identity

scheduler_bp = Blueprint('scheduler', __name__)


@scheduler_bp.route('/v1/api/admin/schedules', methods=['GET'])
@authed
@admin
def list_schedules():
    print("here")
    repo = ScheduledJobRepository()
    response = repo.get_scheduled_jobs()
    if response.success:
        return {
            'success': True,
            'data': ReadScheduledJobSchema(many=True).dump(response.data)
        }
    return {
        'success': False
    }


@scheduler_bp.route('/v1/api/admin/schedules', methods=['POST'])
@authed
@admin
def create_schedule():
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
        }
    except ValidationError as error:
        return error.messages, 400
    except Exception:
        abort(500)


@scheduler_bp.route('/v1/api/admin/schedules/<schedule_id>', methods=['PUT'])
@authed
@admin
def update_schedule(schedule_id):
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
        }
    except ValidationError as error:
        return error.messages, 400
    except Exception:
        abort(500)


@scheduler_bp.route('/v1/api/admin/schedules/<schedule_id>', methods=['DELETE'])
@authed
@admin
def delete_schedule(schedule_id):
    repo = ScheduledJobRepository()
    result = ScheduledJobRepository.get_scheduled_job_by_id(schedule_id)
    if result.success:
        repo.delete_scheduled_job(result.data)
        return {
            'success': True
        }
    return {
        'success': False
    }


@scheduler_bp.route('/v1/api/admin/schedules/<schedule_id>/run', methods=['POST'])
@authed
@admin
def run_schedule():
    return {
        'success': False
    }


@scheduler_bp.route('/v1/api/admin/schedules/instants', methods=['GET'])
@authed
@admin
def list_historical_instants():
    repo = ScheduledJobRepository()
    return {
        'success': False
    }

