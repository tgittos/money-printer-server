import json

from flask import Blueprint, request

from core.apis.plaid.common import PlaidApiConfig
from core.apis.mailgun import MailGunConfig
from core.repositories.plaid_repository import get_repository as get_plaid_repository, UpdatePlaidItem
from core.repositories.holding_repository import get_repository as get_holdings_repository
from core.repositories.account_repository import get_repository as get_account_repository
from core.repositories.balance_repository import get_repository as get_balance_repository
from core.lib.logger import get_logger
from server.config import mysql_config, plaid_config, mailgun_config, iex_config

webhooks_bp = Blueprint('webhooks', __name__)


@webhooks_bp.route('/v1/webhooks/plaid', methods=['POST'])
def receive_plaid_webhook():
    logger = get_logger(__name__)

    plaid_data = json.loads(request.data)
    logger.info("received plaid webhook {0}".format(plaid_data))

    webhook_type = plaid_data['webhook_type']
    webhook_code = plaid_data['webhook_code']
    plaid_item_id = plaid_data['item_id']

    plaid_repo = get_plaid_repository(sql_config=mysql_config, plaid_api_config=plaid_config)
    account_repo = get_account_repository(mysql_config=mysql_config, plaid_config=plaid_config,
                                          mailgun_config=mailgun_config, iex_config=iex_config)
    holding_repo = get_holdings_repository(mysql_config=mysql_config, iex_config=iex_config, plaid_config=plaid_config,
                                           mailgun_config=mailgun_config)
    balance_repo = get_balance_repository(mysql_config=mysql_config, plaid_config=plaid_config, mailgun_config=mailgun_config)

    if webhook_type == "ITEM":
        if webhook_code == "ERROR":
            error = plaid_data['error']
            if error['error_type'] == 'OAUTH_ERROR':
                plaid_repo.update_plaid_item(UpdatePlaidItem(
                    id=plaid_item_id,
                    status=error['error_code']
                ))

        if webhook_code == "NEW_ACCOUNTS_AVAILABLE":
            account_repo.schedule_account_sync_by_plaid_item_id(remote_plaid_item_id=plaid_item_id)

    if webhook_type == "TRANSACTIONS":
        if webhook_code == "INITIAL_UPDATE":
            account_repo.schedule_account_sync_by_plaid_item_id(remote_plaid_item_id=plaid_item_id)

        if webhook_code == "DEFAULT_UPDATE":
            balance_repo.schedule_update_all_balances(plaid_item_id=plaid_item_id)

    if webhook_type == "HOLDINGS":
        if webhook_code == "DEFAULT_UPDATE":
            holding_repo.schedule_update_holdings(plaid_item_id=plaid_item_id)

    if webhook_type == "INVESTMENT_TRANSACTIONS":
        if webhook_code == "DEFAULT_UPDATE":
            holding_repo.schedule_update_transactions(plaid_item_id=plaid_item_id)

    return {
        'success': False
    }

