from __future__ import with_statement

import re

from base import TestCase, MyForm


class TestValidateOnSubmit(TestCase):

    def test_not_submitted(self):
        response = self.client.get("/")
        assert 'DANNY' not in response.data

    def test_submitted_not_valid(self):
        self.app.config['CSRF_ENABLED'] = False
        response = self.client.post("/", data={})
        assert 'DANNY' not in response.data

    def test_submitted_and_valid(self):
        self.app.config['CSRF_ENABLED'] = False
        response = self.client.post("/", data={"name": "danny"})
        assert 'DANNY' in response.data


class TestValidateWithoutSubmit(TestCase):

    def test_unsubmitted_valid(self):
        class obj:
            name = "foo"
        assert MyForm(obj=obj, csrf_enabled=False).validate()
        fake_session = {}
        t = MyForm(csrf_context=fake_session).generate_csrf_token(fake_session)
        assert MyForm(obj=obj, csrf_token=t, csrf_context=fake_session).validate()


class TestHiddenTag(TestCase):

    def test_hidden_tag(self):

        response = self.client.get("/hidden/")
        assert response.data.count('type="hidden"') == 5
        assert 'name="_method"' in response.data


class TestCSRF(TestCase):

    def test_csrf_token(self):

        response = self.client.get("/")
        assert '<div style="display:none;"><input id="csrf_token" name="csrf_token" type="hidden" value' in response.data

    def test_invalid_csrf(self):

        response = self.client.post("/", data={"name": "danny"})
        assert 'DANNY' not in response.data
        assert "CSRF token missing" in response.data

    def test_csrf_disabled(self):

        self.app.config['CSRF_ENABLED'] = False

        response = self.client.post("/", data={"name": "danny"})
        assert 'DANNY' in response.data

    def test_validate_twice(self):

        response = self.client.post("/simple/", data={})
        self.assert_200(response)

    def test_ajax(self):

        response = self.client.post("/ajax/",
                                    data={"name": "danny"},
                                    headers={'X-Requested-With': 'XMLHttpRequest'})

        assert response.status_code == 200

    def test_valid_csrf(self):

        response = self.client.get("/")
        pattern = re.compile(r'name="csrf_token" type="hidden" value="([0-9a-z#A-Z-]*)"')
        match = pattern.search(response.data)
        assert match

        csrf_token = match.groups()[0]

        response = self.client.post("/", data={"name": "danny",
                                               "csrf_token": csrf_token})
        assert "DANNY" in response.data

    def test_double_csrf(self):

        response = self.client.get("/")
        pattern = re.compile(r'name="csrf_token" type="hidden" value="([0-9a-z#A-Z-]*)"')
        match = pattern.search(response.data)
        assert match

        csrf_token = match.groups()[0]

        response = self.client.post("/two_forms/", data={"name": "danny",
                                                         "csrf_token": csrf_token})
        assert response.data == "OK"
