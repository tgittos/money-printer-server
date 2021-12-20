from flask import Blueprint, request, Response, abort
from marshmallow import ValidationError

from core.models.scheduler.scheduled_job import ScheduledJobSchema, CreateScheduledJobSchema
from core.repositories.scheduled_job_repository import ScheduledJobRepository
from .decorators import authed, admin, get_identity

scheduler_bp = Blueprint('scheduler', __name__)


@scheduler_bp.route('/v1/api/admin/schedules', methods=['GET'])
@authed
@admin
def list_schedules():
    repo = ScheduledJobRepository()
    scheduled = repo.get_scheduled_jobs()
    if scheduled:
        return {
            'success': True,
            'data': ScheduledJobSchema(many=True).dump(scheduled)
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
        job = repo.create_scheduled_job(schema)

        if job:
            return {
                'success': True,
                'data': ScheduledJobSchema().dump(job)
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
        schema = ScheduledJobSchema().load(request.json)

        repo = ScheduledJobRepository()
        job = repo.get_scheduled_job_by_id(schedule_id)

        if job:
            job.job_name = schema.get('job_name') or job.job_name
            job.cron = schema.get('cron') or job.cron
            job.json_args = schema.get('json_args') or job.json_args
            job.active = schema.get('active') or job.active

            repo.update_scheduled_job(job)

            return {
                'success': True,
                'data': ScheduledJobSchema().dump(job)
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
    job = ScheduledJobRepository.get_scheduled_job_by_id(schedule_id)
    repo.delete_scheduled_job(job)
    return {
        'success': True
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

