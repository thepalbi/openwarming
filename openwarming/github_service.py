import requests

class UserNotFound(Exception):
    def errorMessage(self):
        return "invalid_github_user"

class UserWithoutLocation(Exception):
    def errorMessage(self):
        return "user_has_no_location_defined"

class APIError(Exception):
    def errorMessage(self):
        return "error_in_api_request"

def getUserLocation(anUsername):
    response = requests.get("https://api.github.com/users/" + anUsername)
    userData = response.json()

    if response.status_code == 404 and\
        "message" in userData and\
        userData["message"] == "Not Found":
        raise UserNotFound

    if response.status_code != 200:
        raise APIError

    if userData["location"] is None:
        raise UserWithoutLocation

    return userData["location"]

def getUserReposCreationDates(anUsername):
    response = requests.get("https://api.github.com/users/" + anUsername + "/repos")
    reposData = response.json()

    if response.status_code == 404 and\
        "message" in reposData and\
        reposData["message"] == "Not Found":
        raise UserNotFound

    if response.status_code != 200:
        raise APIError

    reposCreationDates = []

    for repoData in reposData:
        reposCreationDates.append(repoData["created_at"])

    return reposCreationDates