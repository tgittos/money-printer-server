from prometheus_client import metrics

from core.lib.logger import get_logger
from core.stores.mysql import MySql
from core.apis.plaid.oauth import PlaidOauth
from core.apis.plaid.common import PLAID_PRODUCTS_STRINGS
from core.models import PlaidItem
from core.schemas import CreatePlaidItemSchema

# import all the actions so that consumers of the repo can access everything
import core.actions.plaid.crud as crud
from core.repositories.repository_response import RepositoryResponse

from config import mysql_config


class PlaidRepository:

    db = MySql(mysql_config)
    logger = get_logger(__name__)
    api = PlaidOauth()

    def info(self, profile_id: int) -> RepositoryResponse:
        """
        Returns the Plaid specific information for the given profile.
        """
        with self.db.get_session() as session:
            plaid_item = session.query(PlaidItem).where(
                PlaidItem.profile_id == profile_id).first()

        if plaid_item is None:
            return RepositoryResponse(
                success=False,
                message=f"Could not find PlaidItem for profile with ID {profile_id}"
            )

        return RepositoryResponse(
            success=True,
            data={
                'item_id': plaid_item.item_id,
                'access_token': plaid_item.access_token,
                'products': PLAID_PRODUCTS_STRINGS
            }
        )

    def create_link_token(self, profile_id: int, webhook_host: str) -> RepositoryResponse:
        """
        Calls into the Plaid API to fetch a link token for the user to auth with Plaid.
        """
        try:
            plaid_link_result = self.api.create_link_token(webhook_host)
            print('link result:', plaid_link_result)
            if plaid_link_result is None:
                return RepositoryResponse(
                    success=False,
                    message=f"Unknown error from Plaid creating link token"
                )
            return RepositoryResponse(
                success=True,
                data={
                    # manually list this out so I know the shape without
                    # looking at the code again
                    'link_token': plaid_link_result['link_token'],
                    'created_at': plaid_link_result['created_at'],
                    'expiration': plaid_link_result['expiration'],
                    'metadata': plaid_link_result['metadata'],
                    'request_id': plaid_link_result['request_id'],
                    'item_id': plaid_link_result['item_id']
                }
            )
        except Exception:
            return RepositoryResponse(
                success=False,
                message=f"Unknown error from Plaid creating link token"
            )

    def get_access_token(self, profile_id: int, public_token: str) -> RepositoryResponse:
        """
        Exchanges the public token Plaid gave the user after auth with a private access token.
        """
        try:
            plaid_access_result = self.api.get_access_token(public_token)
            if plaid_access_result is None:
                return RepositoryResponse(
                    success=False,
                    message=f"Unknown error from Plaid exchanging public token"
                )

            print(plaid_access_result)
            # create a plaid token if it's valid
            create_link_result = crud.create_plaid_item(
                self.db, profile_id, CreatePlaidItemSchema().load(plaid_access_result))

            if not create_link_result.success:
                return RepositoryResponse(
                    success=False,
                    message=f"Successfully got access token, failed to save to the DB"
                )

            return RepositoryResponse(
                success=True,
                data={
                    'access_token': create_link_result.data.access_token,
                    'item_id': create_link_result.data.item_id,
                    'request_id': create_link_result.data.request_id
                }
            )
        except Exception:
            return RepositoryResponse(
                success=False,
                message=f"Unknown error from Plaid exchanging public token"
            )

    def get_plaid_item_by_id(self, profile_id: int, id: int) -> RepositoryResponse:
        """
        Return the Plaid Item from the DB by it's ID
        """
        return crud.get_plaid_item_by_id(self.db, profile_id, id)
