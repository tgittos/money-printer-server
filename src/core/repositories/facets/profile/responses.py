from core.models.profile import Profile


class AuthResponse:
    def __init__(self, profile: Profile, token: str):
        self.profile = profile
        self.token = token