from . import handlers
import tornado.web
import logging

class Server(tornado.web.Application):
    def __init__(self, **kwargs):
        api_handlers = [
            ("/temperatures/(.*)", handlers.TemperatureHandler)
        ]
        logging.debug(api_handlers)
        super(Server, self).__init__(api_handlers, **kwargs)