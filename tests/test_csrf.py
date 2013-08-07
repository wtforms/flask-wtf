from __future__ import with_statement

import re
from flask.ext.wtf.csrf import csrf_protect
from .base import TestCase, to_unicode

csrf_token_input = re.compile(
    r'name="csrf_token" type="hidden" value="([0-9a-z#A-Z-]*)"'
)


def get_csrf_token(data):
    match = csrf_token_input.search(to_unicode(data))
    assert match
    return match.groups()[0]


class TestCSRF(TestCase):
    def setUp(self):
        self.app = self.create_app()
        self.app.config['WTF_CSRF_SECRET_KEY'] = "a poorly kept secret."
        csrf_protect(self.app)
        self.client = self.app.test_client()

    def test_invalid_csrf(self):
        response = self.client.post("/", data={"name": "danny"})
        assert response.status_code == 400

    def test_valid_csrf(self):
        response = self.client.get("/")
        csrf_token = get_csrf_token(response.data)

        response = self.client.post("/", data={
            "name": "danny",
            "csrf_token": csrf_token
        })
        assert "DANNY" in to_unicode(response.data)
