from core.models.profile import Profile


class CreatePlaidItem:

    def __init__(self, profile: Profile, item_id: str, access_token: str, request_id: str):
        self.profile = profile
        self.item_id = item_id
        self.access_token = access_token
        self.request_id = request_id
