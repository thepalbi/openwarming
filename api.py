import requests
import tornado.ioloop
import tornado.web
import traceback

class UserNotFound(Exception):
    def errorMessage(self):
        return "invalid_github_user"

class UserWithoutLocation(Exception):
    def errorMessage(self):
        return "user_has_no_location_defined"

class APIError(Exception):
    def errorMessage(self):
        return "error_in_github_api"

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

class TemperatureHandler(tornado.web.RequestHandler):
    def get(self, ghUser):
        userLocation = None

        try:
            userLocation = getUserLocation(ghUser)

            print(getUserReposCreationDates(ghUser))
        except (UserNotFound, APIError, UserWithoutLocation) as e:
            self.set_status(404)
            self.write(e.errorMessage())
            return
        except Exception as e:
            self.set_status(500)
            self.write("unhandled_exception")
            print("Unhandled exception: " + str(e) + f'\nStackTrace: {traceback.format_exc()}')
            return

        self.write(userLocation)

def make_app():
    return tornado.web.Application([
        ("/temperatures/(.*)", TemperatureHandler)
    ])

if __name__ == "__main__":
    DEFAULT_PORT = 8888
    app = make_app()
    app.listen(DEFAULT_PORT)
    print(f'Serving openWarming API in localhost:{DEFAULT_PORT}')
    tornado.ioloop.IOLoop.current().start().start()


