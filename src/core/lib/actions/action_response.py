class ActionResponse:

    def __init__(self, success, data=None, message=''):
        self.success = success
        self.data = data
        self.message = message
