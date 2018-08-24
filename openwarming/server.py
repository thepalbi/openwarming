from . import handlers
import tornado.web

class Server(tornado.web.Application):
    def __init__(self, **kwargs):
        api_handlers = [
        ("/temperatures/(.*)", handlers.TemperatureHandler)
    ]