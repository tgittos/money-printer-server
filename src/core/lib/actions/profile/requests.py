from core.models.profile import Profile


class RegisterProfileRequest:
    def __init__(self, email: str, first_name: str, last_name: str):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name


class ResetProfilePasswordRequest:
    def __init__(self, profile: Profile, token: str, password: str):
        self.profile = profile
        self.token = token
        self.password = password


class LoginRequest:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password
