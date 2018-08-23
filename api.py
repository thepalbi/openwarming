import requests
import tornado.ioloop
import tornado.web
import traceback
from openwarming import github_service

# t % curl -v 'http://api.worldweatheronline.com/premium/v1/past-weather.ashx?key=d865b95a583447a593b210600182308&q=Argentina&format=json&date=2018-04-11'|jq "."
WEATHER_API_KEY = "d865b95a583447a593b210600182308"

def getDateAverageTemperature(aDate, aLocation):
    # Add date format
    formattedDate = aDate
    # URLEncode location
    response = requests.get("http://api.worldweatheronline.com/premium/v1/past-weather.ashx" +\
        f'?key={WEATHER_API_KEY}&q={aLocation}&format=json&date={formattedDate}')

    if response.status_code != 200:
        # TODO: Add more error description in API Error class
        raise APIError

    # .data.weather[0].maxtempC
    # .data.weather[0].mintempC
    weatherData = response.json()["data"]["weather"][0]

    maxTemp = float(weatherData["maxtempC"])
    minTemp = float(weatherData["mintempC"])

    return (maxTemp + minTemp) / 2

class TemperatureHandler(tornado.web.RequestHandler):
    def get(self, ghUser):
        userLocation = None

        try:
            userLocation = github_service.getUserLocation(ghUser)
            # print(getUserReposCreationDates(ghUser))
            print(getDateAverageTemperature("2018-04-12", "Argentina"))
        except (github_service.UserNotFound, github_service.APIError, github_service.UserWithoutLocation) as e:
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


