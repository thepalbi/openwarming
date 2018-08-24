from .server import Server

from tornado.testing import AsyncHTTPTestCase
import tornado

import logging
logging.basicConfig(level=logging.DEBUG)

import unittest
import json

def parseResponseBody(response):
    return json.loads(response.body.decode("utf8"))


class ApiTestCase(AsyncHTTPTestCase):
    def get_app(self):
        self.app = Server(debug=True)
        return self.app

    def test_non_existent_github_user(self):
        response = self.fetch(self.get_url('/temperatures/ndoawocnaowx'),method='GET')
        self.assertEqual(response.code,404)
        responseBody = parseResponseBody(response)
        self.assertEqual(responseBody["message"], "invalid_github_user" )

if __name__ == '__main__':
    unittest.main()