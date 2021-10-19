from flask import Blueprint, abort

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
            'data': [s.to_dict for s in scheduled]
        }
    return {
        'success': False
    }


@scheduler_bp.route('/v1/api/admin/schedules', methods=['POST'])
@authed
@admin
def create_schedule():
    return {
        'success': False
    }


@scheduler_bp.route('/v1/api/admin/schedules/<schedule_id>', methods=['PUT'])
@authed
@admin
def update_schedule():

    return {
        'success': False
    }


@scheduler_bp.route('/v1/api/admin/schedules/<schedule_id>', methods=['DELETE'])
@authed
@admin
def delete_schedule():
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
    return {
        'success': False
    }

