from __future__ import with_statement

import re
from flask import render_template
from flask.ext.wtf.csrf import CsrfProtect
from flask.ext.wtf.csrf import validate_csrf, generate_csrf
from .base import TestCase, MyForm, to_unicode

csrf_token_input = re.compile(
    r'name="csrf_token" type="hidden" value="([0-9a-z#A-Z-\.]*)"'
)


def get_csrf_token(data):
    match = csrf_token_input.search(to_unicode(data))
    assert match
    return match.groups()[0]


class TestCSRF(TestCase):
    def setUp(self):
        app = self.create_app()
        app.config['WTF_CSRF_SECRET_KEY'] = "a poorly kept secret."
        csrf = CsrfProtect(app, self.csrf_hook)

        self.csrf_count = 0

        @csrf.exempt
        @app.route('/csrf-exempt', methods=['GET', 'POST'])
        def csrf_exempt():
            form = MyForm()
            if form.validate_on_submit():
                name = form.name.data.upper()
            else:
                name = ''

            return render_template(
                "index.html", form=form, name=name
            )

        self.app = app
        self.client = self.app.test_client()

    def csrf_hook(self, request):
        self.csrf_count += 1

    def test_invalid_csrf(self):
        response = self.client.post("/", data={"name": "danny"})
        assert response.status_code == 400
        assert self.csrf_count

    def test_valid_csrf(self):
        response = self.client.get("/")
        csrf_token = get_csrf_token(response.data)

        response = self.client.post("/", data={
            "name": "danny",
            "csrf_token": csrf_token
        })
        assert "DANNY" in to_unicode(response.data)

    def test_csrf_exempt(self):
        response = self.client.get("/csrf-exempt")
        csrf_token = get_csrf_token(response.data)

        response = self.client.post("/csrf-exempt", data={
            "name": "danny",
            "csrf_token": csrf_token
        })
        assert "DANNY" in to_unicode(response.data)

    def test_validate_csrf(self):
        with self.app.test_request_context():
            assert not validate_csrf('ff##dd')
            csrf_token = generate_csrf()
            assert validate_csrf(csrf_token)
