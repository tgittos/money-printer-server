from flask import Blueprint
from flask import request
import json

from core.apis.plaid.common import PlaidApiConfig
from core.repositories.account_repository import *

from server.services.api.routes.decorators import authed, get_identity


# define the blueprint for plaid oauth
account_bp = Blueprint('account', __name__)

@account_bp.route('/v1/api/accounts', methods=['GET'])
@authed
def list_accounts():
    user = get_identity()
    repo = get_repository()
    if user is not None and user['id'] is not None:
        accounts = repo.get_all_accounts_by_profile(user['id'])
        if accounts is not None:
            return {
                'success': True,
                'data': [a.to_dict() for a in accounts]
            }
    return {
        'success': False
    }
