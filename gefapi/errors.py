"""GEF API ERRORS"""


class Error(Exception):

    def __init__(self, message):
        self.message = message

    @property
    def serialize(self):
        return {
            'message': self.message
        }


class UserNotFound(Error):
    pass


class UserDuplicated(Error):
    pass


class InvalidFile(Error):
    pass
