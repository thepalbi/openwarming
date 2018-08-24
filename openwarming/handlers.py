import tornado.web
import traceback
from . import github_service, weather_service
from .exceptions import *

class TemperatureHandler(tornado.web.RequestHandler):
    def get(self, ghUser):
        userLocation = None
        userReposCreationDates = None
        try:
            userLocation = github_service.getUserLocation(ghUser)
            userReposCreationDates = github_service.getUserReposCreationDates(ghUser)
        except (UserNotFound, UserWithoutLocation) as e:
            self.set_status(404)
            self.writeExceptionMessage(e.errorMessage())
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

        self.set_status(200)
        self.write(self.writeResponse(reposCount, reposTemps))

    def writeResponse(self, aReposCount, reposTemps):
        return {
            "repositoriesCount": aReposCount,
            "avgTemperatures": reposTemps
        }

    def writeExceptionMessage(self, message):
        self.write({
            "message": message
        })

    def handleUnexpectedException(self, e):
        self.set_status(500)
        self.writeExceptionMessage("unhandled_exception - %s" % (e.__class__.__name__))
        print("Unhandled exception: " + str(e) + f'\nStackTrace: {traceback.format_exc()}')


