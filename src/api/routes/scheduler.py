from flask import Blueprint, request, Response

from core.models.scheduler.scheduled_job import ScheduledJobSchema
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
    job_name = request.json.get('jobName')
    cron = request.json.get('cron')
    args = request.json.get('args')

    repo = ScheduledJobRepository()
    schema = ScheduledJobSchema().load({
        'job_name':job_name,
        'cron':cron,
        'args':args
    })
    job = repo.create_scheduled_job(schema)

    if job:
        return {
            'success': True,
            'data': ScheduledJobSchema().dump(job)
        }

    return {
        'success': False
    }


@scheduler_bp.route('/v1/api/admin/schedules/<schedule_id>', methods=['PUT'])
@authed
@admin
def update_schedule(schedule_id):
    if not request.json:
        return Response({
            "success": False
        }, status=400, mimetype='application/json')

    job_name = request.json.get('job_name')
    cron = request.json.get('cron')
    json_args = request.json.get('json_args')
    active = request.json.get('active')

    repo = ScheduledJobRepository()
    job = repo.get_scheduled_job_by_id(schedule_id)

    if job:
        job.job_name = job_name or job.job_name
        job.cron = cron or job.cron
        job.json_args = json_args or job.json_args
        job.active = active or job.active

        repo.update_scheduled_job(job)

        return {
            'success': True,
            'data': ScheduledJobSchema().dump(job)
        }

    return {
        'success': False
    }


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

