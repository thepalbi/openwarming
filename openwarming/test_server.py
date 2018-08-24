from .server import Server

from tornado.testing import AsyncHTTPTestCase
import tornado

import logging
logging.basicConfig(level=logging.DEBUG)

import unittest
import json

def parseResponseBody(response):
    return json.loads(response.body.decode("utf8"))

"""
TODO: A big one. Instead of making the actual requests to Github and Weather API's, find a way
to mock the up. This would allow to make tests more deterministic, save the API keys entries,
and make the test suite preety much faster.
"""

class ApiTestCase(AsyncHTTPTestCase):
    def get_app(self):
        self.app = Server(debug=True)
        return self.app

    def test_non_existent_github_user(self):
        response = self.fetch(self.get_url('/temperatures/ndoawocnaowx'),method='GET')
        self.assertEqual(response.code,404)
        responseBody = parseResponseBody(response)
        self.assertEqual(responseBody["message"], "invalid_github_user" )

    def test_user_without_location_defined(self):
        response = self.fetch(self.get_url('/temperatures/npazosmendez'),method='GET')
        self.assertEqual(response.code,404)
        responseBody = parseResponseBody(response)
        self.assertEqual(responseBody["message"], "user_has_no_location_defined" )

if __name__ == '__main__':
    unittest.main()