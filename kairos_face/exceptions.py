class SettingsNotPresentException(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __repr__(self):
        return self.msg

    def __str__(self):
        return self.__repr__()


class ServiceRequestError(Exception):
    def __init__(self, status_code, response_msg, payload):
        self.status_code = status_code
        self.response_msg = response_msg
        self.payload = payload

    def __repr__(self):
        return str(self.response_msg)

    def __str__(self):
        return self.__repr__()
