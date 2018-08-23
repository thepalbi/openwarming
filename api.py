import requests
import tornado.ioloop
import tornado.web

class UserNotFound(Exception):
    def errorMessage(self):
        return "invalid_github_user"


class APIError(Exception):
    def errorMessage(self):
        return "error_in_github_api"

def getUserLocation(anUsername):
    response = requests.get("https://api.github.com/users/" + anUsername)
    userData = response.json()

    if response.status_code != 200:
        raise APIError

    if "message" in userData and\
        userData["message"] == "Not Found":
        raise UserNotFound

    return userData["location"]

class TemperatureHandler(tornado.web.RequestHandler):
    def get(self, ghUser):
        userLocation = None

        try:
            userLocation = getUserLocation(ghUser)
        except (UserNotFound, APIError) as e:
            self.set_status(404)
            self.write(e.errorMessage())
            return
        except Exception as e:
            self.set_status(500)
            self.write("Unhandled exception: " + str(e))
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


