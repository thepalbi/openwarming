import requests
import dateutil.parser
from .exceptions import *
import cachetools

usersCache = cachetools.TTLCache(maxsize=100, ttl=3600)
reposCache = cachetools.TTLCache(maxsize=100, ttl=3600)

@cachetools.cached(usersCache)
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
@cachetools.cached(reposCache)
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