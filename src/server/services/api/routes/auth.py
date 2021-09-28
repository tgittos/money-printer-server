from flask import Blueprint
from flask import request
import json

from core.repositories.profile_repository import ProfileRepository, RegisterProfileRequest, LoginRequest
from .decorators import authed
from config import mysql_config, mailgun_config

# define the blueprint for plaid oauth
auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/v1/api/auth/register', methods=['POST'])
def register():
    username = request.json['username']
    first_name = request.json['firstName']
    last_name = request.json['lastName']

    repo = ProfileRepository()

    result = repo.register(RegisterProfileRequest(
        first_name=first_name,
        last_name=last_name,
        email=username
    ))

    return result.to_dict


@auth_bp.route('/v1/api/auth/unauthenticated', methods=['GET'])
def get_unauthenticated_user():
    repo = ProfileRepository()
    result = repo.get_unauthenticated_user()
    if result is None:
        return {
            'message': 'No unauthenticated user configured'
        }, 404
    return ({
        'success': True,
        'data': result
    })


@auth_bp.route('/v1/api/auth/login', methods=['POST'])
def login():
    username = request.json['username']
    password = request.json['password']
    repo = ProfileRepository()
    result = repo.login(LoginRequest(
        email=username,
        password=password
    ))

    if result is None:
        return {
            'success': False,
            'message': 'Username/password combination not found'
        }, 404

    return {
        'success': True,
        'data': result
    }


@auth_bp.route('/v1/api/auth/logout', methods=['POST'])
@authed
def logout():
    username = request.json['username']
    repo = ProfileRepository()
    result_json = repo.logout(username=username)

    return result_json


@auth_bp.route('/v1/api/auth/reset', methods=['POST'])
def reset_password():
    username = request.json['username']
    repo = ProfileRepository()
    result_json = repo.reset_password(username=username)
    return result_json


@auth_bp.route('/v1/api/auth/reset/continue', methods=['POST'])
def continue_reset_password():
    username = request.json['username']
    token = request.json['token']
    new_password = request.json['password']
    repo = ProfileRepository()
    result = repo.continue_reset_password(username=username, token=token, password=new_password)
    return result

