from core.repositories.profile_repository import get_repository as get_profile_repository
from core.repositories.plaid_repository import get_repository as get_plaid_repository, GetPlaidItem
from core.apis.plaid.auth import Auth

class SyncAccounts:

    def __init__(self, redis_message):
        self.profile_id = redis_message['profile_id']
        self.plaid_link_id = redis_message['plaid_link_id']
        self.plaid_repo = get_plaid_repository()

    def run(self):
        profile = self.__fetch_profile()
        plaid_link = self.__fetch_plaid_link()
        plaid_auth_api = Auth()
        plaid_auths = plaid_auth_api.get_auth(plaid_link.access_token)


    def __fetch_profile(self):
        repo = get_profile_repository()
        return repo.get_by_id(self.profile_id)

    def __fetch_plaid_link(self):
        return self.plaid_repo.get_plaid_item(GetPlaidItem(
            item_id=self.plaid_link_id
        ))

