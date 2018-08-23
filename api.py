import requests
import tornado.ioloop
import tornado.web
import traceback
from openwarming import github_service, weather_service

class TemperatureHandler(tornado.web.RequestHandler):
    def get(self, ghUser):
        userLocation = None
        userReposCreationDates = None
        temperatures = {}
        try:
            userLocation = github_service.getUserLocation(ghUser)
            userReposCreationDates = github_service.getUserReposCreationDates(ghUser)

            for repoCreationDate in userReposCreationDates:
                temperatures[str(repoCreationDate)] = weather_service.getDateAverageTemperature(repoCreationDate, userLocation)

        except (github_service.UserNotFound, github_service.APIError, github_service.UserWithoutLocation) as e:
            self.set_status(404)
            self.write(e.errorMessage())
            return
        except Exception as e:
            self.set_status(500)
            self.write("unhandled_exception")
            print("Unhandled exception: " + str(e) + f'\nStackTrace: {traceback.format_exc()}')
            return

        self.write(temperatures)

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