import requests
import dateutil.parser
from .exceptions import *

def getUserLocation(anUsername):
    response = requests.get("https://api.github.com/users/" + anUsername)
    userData = response.json()

    if response.status_code == 404 and\
        "message" in userData and\
        userData["message"] == "Not Found":
        raise UserNotFound

    if response.status_code != 200:
        raise APIError(response)

    if userData["location"] is None:
        raise UserWithoutLocation

    return userData["location"]

# TODO: Sort dates in increasing order
def getUserReposCreationDates(anUsername):
    response = requests.get("https://api.github.com/users/" + anUsername + "/repos")
    reposData = response.json()

    if response.status_code == 404 and\
        "message" in reposData and\
        reposData["message"] == "Not Found":
        raise UserNotFound

    if response.status_code != 200:
        raise APIError(response)

    reposCreationDates = []

    for repoData in reposData:
        stringDate = repoData["created_at"]
        reposCreationDates.append(dateutil.parser.parse(stringDate))

    return reposCreationDates