import tornado.web
import traceback
from . import github_service, weather_service

class TemperatureHandler(tornado.web.RequestHandler):
    def get(self, ghUser):
        userLocation = None
        userReposCreationDates = None
        try:
            userLocation = github_service.getUserLocation(ghUser)
            userReposCreationDates = github_service.getUserReposCreationDates(ghUser)
        except (github_service.UserNotFound, github_service.APIError, github_service.UserWithoutLocation) as e:
            self.set_status(404)
            self.write(e.errorMessage())
            return
        except Exception as e:
            self.handleUnexpectedException(e)
            return

        reposCount = len(userReposCreationDates)
        reposTemps = []

        for repoCreationDate in userReposCreationDates:
            averageTemperature = None
            try:
                averageTemperature = weather_service.getDateAverageTemperature(repoCreationDate, userLocation)
            # TODO: Handle this exception in some other way, to show some possible cause.
            # No 404 returned, since this is independant of the input the endpoint recieves from
            # the user.
            except Exception as e:
                self.handleUnexpectedException(e)
                return

            reposTemps.append(averageTemperature)

        self.write({
            "repositoriesCount": reposCount,
            "avgTemperatures": reposTemps
        })

    def handleUnexpectedException(self, e):
        self.set_status(500)
        self.write("unhandled_exception")
        print("Unhandled exception: " + str(e) + f'\nStackTrace: {traceback.format_exc()}')

