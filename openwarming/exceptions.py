class UserNotFound(Exception):
    def errorMessage(self):
        return "invalid_github_user"

class UserWithoutLocation(Exception):
    def errorMessage(self):
        return "user_has_no_location_defined"

class APIError(Exception):
    def __init__(self, aReponseObject):
        self.statusCode = aReponseObject.status_code
        self.responseBody = aReponseObject.text
    def errorMessage(self):
        return "error_in_api_request - statusCode %d - body %s" % (self.statusCode, str(self.responseBody))