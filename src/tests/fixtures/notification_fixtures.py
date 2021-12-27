class MockResponse:
    def __init__(self, status_code):
        self.status_code = status_code


def mock_notify_profile_created(mgcfg, request):
    return MockResponse(status_code=200)