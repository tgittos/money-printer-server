from flask import Blueprint
from flask import request
import json

from core.repositories.profile_repository import *

from server.config import config as server_config
from server import load_config
app_config = load_config()


def get_repository():
    repo = ProfileRepository(ProfileRepositoryConfig(
        mailgun_config=MailGunConfig(api_key=server_config['mailgun']['api_key'],
                                     domain=server_config['mailgun']['domain']),
        mysql_config=app_config['db']
    ))
    return repo


# define the blueprint for plaid oauth
auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/v1/api/auth/register', methods=['POST'])
def register():
    print("request.json: {0}".format(request.json))
    username = request.json['username']
    first_name = request.json['firstName']
    last_name = request.json['lastName']

    repo = get_repository()

    result = repo.register(RegisterProfileRequest(
        first_name=first_name,
        last_name=last_name,
        email=username
    ))

    return result.to_dict

@auth_bp.route('/v1/api/auth/unauthenticated', methods=['GET'])
def get_unauthenticated_user():
    repo = get_repository()
    result = repo.get_unauthenticated_user()
    if result is None:
        return ({
            'success': False,
            'message': 'No unauthenticated user configured'
        })
    return ({
        'success': True,
        'data': result.to_dict()
    })

@auth_bp.route('/v1/api/auth/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']
    repo = get_repository()
    result_json = repo.login(LoginRequest(
        username=username,
        password=password
    ))

    return result_json

@auth_bp.route('/v1/api/auth/logout', methods=['POST'])
def logout():
    username = request.form['username']
    repo = get_repository()
    result_json = repo.logout(username=username)

    return result_json

@auth_bp.route('/v1/api/auth/reset', methods=['POST'])
def reset_password():
    username = request.form['username']
    repo = get_repository()
    result_json = repo.reset_password(username=username)
    return result_json
