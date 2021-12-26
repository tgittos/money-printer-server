from flask import Blueprint
from flask import request

from core.repositories.account_repository import AccountRepository
from core.repositories.plaid_repository import PlaidRepository, PLAID_PRODUCTS_STRINGS
from .decorators import authed, get_identity

from api.lib.constants import API_PREFIX
from api.metrics.plaid_metrics import *


# define the blueprint for plaid oauth
oauth_bp = Blueprint('plaid_oauth', __name__)


@oauth_bp.route(f"/{API_PREFIX}/plaid/info", methods=['GET'])
@authed
@PERF_PLAID_INFO.time()
def info():
    """
    ---
    get:
      summary: Retrieve the current Profile's Plaid auth token
      responses:
        200:
          content:
            application/json:
              schema:
                item_id:
                    type: string
                access_token:
                    type: string
                products:
                    type: array
                    items:
                        type: string
        400:
          content:
            application/json:
              schema:
                success:
                  type: boolean
                message:
                  type: string
      tags:
        - Plaid
    
    """
    repo = PlaidRepository()
    result = repo.info()
    if result.success:
        return result.data

    return {
        'item_id': None,
        'access_token': None,
        'products': PLAID_PRODUCTS_STRINGS
    }


@oauth_bp.route(f"/{API_PREFIX}/plaid/link", methods=['POST'])
@authed
@PERF_PLAID_LINK.time()
def create_link_token():
    """
    ---
    post:
      summary: Generate a link token for the user to auth on our behalf.
      responses:
        200:
          content:
            application/json:
              schema:
                item_id:
                    type: string
                products:
                    type: array
                    items:
                        type: string
        400:
          content:
            application/json:
              schema:
                success:
                  type: boolean
                message:
                  type: string
      tags:
        - Plaid
    """
    base_url = request.base_url
    repo = PlaidRepository()
    result = repo.create_link_token(base_url)
    if result.success:
        return result.data
    return {
        'success': False,
        'message': result.message
    }, 400


@oauth_bp.route(f"/{API_PREFIX}/plaid/access", methods=['POST'])
@authed
@PERF_PLAID_ACCESS.time()
def get_access_token():
    """
    ---
    post:
      summary: Exchange a user's public request token for a private access token
      parameters:
        - in: public_token
          schema:
            type: string
      responses:
        200:
          content:
            application/json:
              schema:
                success:
                    type: boolean
                message:
                    type: string
        400:
          content:
            application/json:
              schema:
                success:
                  type: boolean
                message:
                  type: string
      tags:
        - Plaid
    """
    
    profile = get_identity()
    public_token = request.json['public_token']

    repo = PlaidRepository()
    access_token_result = repo.get_access_token(profile['id'], public_token)
    if not access_token_result.success:
        return access_token_result, 400

    account_repo = AccountRepository()
    schedule_result = account_repo.schedule_account_sync(plaid_item=access_token_result.data)

    if not schedule_result.success:
        return schedule_result, 500

    return {
        'success': access_token_result is not None,
        'message': 'Fetching accounts'
    }
