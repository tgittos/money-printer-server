import json

from flask import Blueprint, request

from core.repositories import PlaidRepository, AccountRepository, HoldingRepository, ProfileRepository
from core.lib.logger import get_logger

from constants import API_PREFIX

webhooks_bp = Blueprint('webhooks', __name__)


@webhooks_bp.route(f"/{API_PREFIX}/webhooks/plaid", methods=['POST'])
def receive_plaid_webhook():
    logger = get_logger(__name__)

    plaid_data = json.loads(request.data)
    logger.info("received plaid webhook {0}".format(plaid_data))

    webhook_type = plaid_data['webhook_type']
    webhook_code = plaid_data['webhook_code']
    plaid_item_id = plaid_data['item_id']

    plaid_repo = PlaidRepository()
    profile_repo = ProfileRepository()
    account_repo = AccountRepository()
    holding_repo = HoldingRepository()

    plaid_item = plaid_repo.get_plaid_item_by_plaid_item_id(plaid_item_id)

    if webhook_type == "ITEM":

        if webhook_code == "ERROR":
            error = plaid_data['error']
            if error['error_type'] == 'OAUTH_ERROR':
                plaid_item.status = error['error_code']
                plaid_repo.update_plaid_item(plaid_item)

        if webhook_code == "NEW_ACCOUNTS_AVAILABLE":
            profile = profile_repo.get_profile_by_id(plaid_item.profile_id)
            profile_repo.schedule_profile_sync(profile=profile)

    if webhook_type == "TRANSACTIONS":
        if webhook_code == "INITIAL_UPDATE":
            profile = profile_repo.get_profile_by_id(plaid_item.profile_id)
            profile_repo.schedule_profile_sync(profile=profile)

        if webhook_code == "DEFAULT_UPDATE":
            account_repo.schedule_update_all_balances(plaid_item=plaid_item)

    if webhook_type == "HOLDINGS":
        if webhook_code == "DEFAULT_UPDATE":
            holding_repo.schedule_update_holdings(plaid_item=plaid_item)

    if webhook_type == "INVESTMENT_TRANSACTIONS":
        if webhook_code == "DEFAULT_UPDATE":
            holding_repo.schedule_update_transactions(plaid_item=plaid_item)

    return {
        'success': True
    }
