from __future__ import with_statement

from flask import g, json

from flask_wtf.csrf import generate_csrf
from .base import MyForm, TestCase, capture_logging, to_unicode


class TestValidateOnSubmit(TestCase):

    def test_not_submitted(self):
        response = self.client.get("/")
        assert b'DANNY' not in response.data

    def test_submitted_not_valid(self):
        self.app.config['WTF_CSRF_ENABLED'] = False
        response = self.client.post("/", data={})
        assert b'DANNY' not in response.data

    def test_submitted_and_valid(self):
        self.app.config['WTF_CSRF_ENABLED'] = False
        response = self.client.post("/", data={"name": "danny"})
        assert b'DANNY' in response.data

    def test_json_data(self):
        self.app.config['WTF_CSRF_ENABLED'] = False
        response = self.client.post(
            '/', content_type='application/json',
            data=json.dumps({'name': 'Flask-WTF'})
        )
        assert b'FLASK-WTF' in response.data


class TestValidateWithoutSubmit(TestCase):
    def test_unsubmitted_valid(self):
        class obj:
            name = 'foo'

        with self.app.test_request_context():
            assert MyForm(obj=obj, meta={'csrf': False}).validate()
            t = generate_csrf()
            assert MyForm(obj=obj, csrf_token=t).validate()


class TestHiddenTag(TestCase):

    def test_hidden_tag(self):

        response = self.client.get("/hidden/")
        assert to_unicode(response.data).count('type="hidden"') == 5
        assert b'name="_method"' in response.data


class TestCSRF(TestCase):

    def test_csrf_token(self):

        response = self.client.get("/")
        snippet = '<input id="csrf_token" name="csrf_token" type="hidden" value'
        assert snippet in to_unicode(response.data)

    def test_invalid_csrf(self):
        from flask_wtf.csrf import logger

        with capture_logging(logger) as handler:
            response = self.client.post("/", data={"name": "danny"})

        assert b'DANNY' not in response.data
        assert b'The CSRF token is missing.' in response.data
        self.assertEqual(1, len(handler))
        self.assertEqual('The CSRF token is missing.', handler[0].message)

    def test_csrf_disabled(self):

        self.app.config['WTF_CSRF_ENABLED'] = False

        response = self.client.post("/", data={"name": "danny"})
        assert b'DANNY' in response.data

    def test_validate_twice(self):

        response = self.client.post("/simple/", data={})
        assert response.status_code == 200

    def test_ajax(self):

        response = self.client.post(
            "/ajax/", data={"name": "danny"},
            headers={'X-Requested-With': 'XMLHttpRequest'}
        )
        assert response.status_code == 200

    def test_valid_csrf(self):
        with self.client:
            self.client.get('/')
            csrf_token = g.csrf_token

        response = self.client.post('/', data={
            'name': 'danny',
            'csrf_token': csrf_token
        })
        assert b'DANNY' in response.data

    def test_double_csrf(self):
        with self.client:
            self.client.get('/')
            csrf_token = g.csrf_token

        response = self.client.post("/two_forms/", data={
            "name": "danny",
            "csrf_token": csrf_token
        })
        assert response.data == b'OK'
