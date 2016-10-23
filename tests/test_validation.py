from __future__ import with_statement

from flask import request

from .base import MyForm, TestCase, to_unicode


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


class TestValidateWithoutSubmit(TestCase):

    def test_unsubmitted_valid(self):
        class obj:
            name = "foo"

        with self.app.test_request_context():
            assert MyForm(obj=obj, csrf_enabled=False).validate()
            fake_session = {}
            t = MyForm(csrf_context=fake_session).generate_csrf_token(
                fake_session
            )
            assert MyForm(
                obj=obj, csrf_token=t,
                csrf_context=fake_session).validate()


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

        response = self.client.post("/", data={"name": "danny"})
        assert b'DANNY' not in response.data
        assert b'CSRF token missing' in response.data

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
            csrf_token = request.csrf_token

        response = self.client.post('/', data={
            'name': 'danny',
            'csrf_token': csrf_token
        })
        assert b'DANNY' in response.data

    def test_double_csrf(self):
        with self.client:
            self.client.get('/')
            csrf_token = request.csrf_token

        response = self.client.post("/two_forms/", data={
            "name": "danny",
            "csrf_token": csrf_token
        })
        assert response.data == b'OK'

    def test_valid_csrf_data(self):
        with self.app.test_request_context():
            assert MyForm().validate_csrf_data(request.csrf_token)
