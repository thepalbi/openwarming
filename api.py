import requests
import json
import tornado.ioloop
import tornado.web
import traceback
from openwarming import github_service, weather_service, handlers

def make_app():
    return tornado.web.Application([
        ("/temperatures/(.*)", handlers.TemperatureHandler)
    ])

if __name__ == "__main__":
    DEFAULT_PORT = 8888
    app = make_app()
    app.listen(DEFAULT_PORT)
    print(f'Serving openWarming API in localhost:{DEFAULT_PORT}')
    tornado.ioloop.IOLoop.current().start().start()