from core.models.profile import Profile


class AuthResponse:
    def __init__(self, profile: Profile, token: str):
        self.profile = profile
        self.token = token

    def to_json(self):
        return {
            'profile': self.profile,
            'token': self.token
        }
