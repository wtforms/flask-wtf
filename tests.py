import unittest

from flask import Flask

class TestCase(unittest.TestCase):

    TESTING = True
    CSRF_ENABLED = False

    def create_app(self):
        
        app = Flask(__name__)
        app.config.from_object(self)
        return app

    def __call__(self, result=None):
        self._pre_setup()
        super(TestCase, self).__call__(result)
        self._post_tearDown()

    def _pre_setup(self):

        self.app = self.create_app()
        self.client = self.app.test_client()
        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def _post_teardown(self):

        self._ctx.pop()


