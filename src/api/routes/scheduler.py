from flask import Blueprint, request

from core.repositories.scheduled_job_repository import ScheduledJobRepository, CreateScheduledJobRequest
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
            'data': [s.to_dict for s in scheduled]
        }
    return {
        'success': False
    }


@scheduler_bp.route('/v1/api/admin/schedules', methods=['POST'])
@authed
@admin
def create_schedule():
    job_name = request.json['jobName']
    cron = request.json['cron']
    args = request.json['args']

    repo = ScheduledJobRepository()
    job = repo.create_scheduled_job(CreateScheduledJobRequest(
        job_name=job_name,
        cron=cron,
        args=args
    ))

    if job:
        return {
            'success': True,
            'data': job.to_dict()
        }

    return {
        'success': False
    }


@scheduler_bp.route('/v1/api/admin/schedules/<schedule_id>', methods=['PUT'])
@authed
@admin
def update_schedule(schedule_id):
    cron = request.json['cron']
    args = request.json['args']

    repo = ScheduledJobRepository()
    job = repo.get_scheduled_job_by_id(schedule_id)

    if job:
        job.cron = cron
        job.args = args

        repo.update_scheduled_job(job)

        return {
            'success': True,
            'data': job.to_dict()
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

