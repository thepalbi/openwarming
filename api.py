import requests
import tornado.ioloop
import tornado.web

class MainHandler(tornado.web.RequestHandler):
    def get(self, ghUser):
        response = requests.get("https://api.github.com/users/" + ghUser)

        if "message" in response.json() and\
            response.json()["message"] == "Not Found":
            self.set_status(404)
            self.write("invalid_github_user")
            return

        self.set_status(200)
        self.write(response.json()["location"])

def make_app():
    return tornado.web.Application([
        ("/temperatures/(.*)", MainHandler)
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start().start()