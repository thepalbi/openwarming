import tornado.web
import traceback
from . import github_service, weather_service

class TemperatureHandler(tornado.web.RequestHandler):
    def get(self, ghUser):
        userLocation = None
        userReposCreationDates = None
        temperatures = []
        try:
            userLocation = github_service.getUserLocation(ghUser)
            userReposCreationDates = github_service.getUserReposCreationDates(ghUser)

            for repoCreationDate in userReposCreationDates:
                averageTemperature = weather_service.getDateAverageTemperature(repoCreationDate, userLocation)
                temperatures.append({
                    "date": str(repoCreationDate),
                    "avgTemperature": averageTemperature
                })

        except (github_service.UserNotFound, github_service.APIError, github_service.UserWithoutLocation) as e:
            self.set_status(404)
            self.write(e.errorMessage())
            return

        except Exception as e:
            self.set_status(500)
            self.write("unhandled_exception")
            print("Unhandled exception: " + str(e) + f'\nStackTrace: {traceback.format_exc()}')
            return

        self.write(json.dumps(temperatures))