import requests
import tornado.ioloop
import tornado.web

class TemperatureHandler(tornado.web.RequestHandler):
    def get(self, ghUser):
        response = requests.get("https://api.github.com/users/" + ghUser)
        userData = response.json()

        if response.status_code != 200:
            self.set_status(404)
            self.write("error_in_github_api")

        if "message" in userData and\
            userData["message"] == "Not Found":
            self.set_status(404)
            self.write("invalid_github_user")
            return

        self.set_status(200)
        self.write(userData["location"])

def make_app():
    return tornado.web.Application([
        ("/temperatures/(.*)", TemperatureHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start().start()