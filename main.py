import tornado.ioloop
from openwarming.server import Server

if __name__ == "__main__":
    DEFAULT_PORT = 8888
    app = Server()
    app.listen(DEFAULT_PORT)
    print(f'Serving openWarming API in localhost:{DEFAULT_PORT}')
    tornado.ioloop.IOLoop.current().start().start()