from __future__ import with_statement

import re
from flask import render_template
from flask_wtf.csrf import CsrfProtect
from flask_wtf.csrf import validate_csrf, generate_csrf
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
        csrf = CsrfProtect(app)
        self.csrf = csrf

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

    def test_invalid_csrf(self):
        response = self.client.post("/", data={"name": "danny"})
        assert response.status_code == 400

        @self.csrf.error_handler
        def invalid(reason):
            return reason

        response = self.client.post("/", data={"name": "danny"})
        assert response.status_code == 200
        assert 'token missing' in to_unicode(response.data)

    def test_valid_csrf(self):
        response = self.client.get("/")
        csrf_token = get_csrf_token(response.data)

        response = self.client.post("/", data={
            "name": "danny",
            "csrf_token": csrf_token
        })
        assert "DANNY" in to_unicode(response.data)

    def test_invalid_secure_csrf(self):
        response = self.client.get("/", base_url='https://localhost/')
        csrf_token = get_csrf_token(response.data)

        response = self.client.post(
            "/",
            data={"name": "danny"},
            headers={'X-CSRFToken': csrf_token},
            base_url='https://localhost/',
        )
        assert response.status_code == 400
        assert "failed" in to_unicode(response.data)

        response = self.client.post(
            "/",
            data={"name": "danny"},
            headers={
                'X-CSRFToken': csrf_token,
            },
            environ_base={
                'HTTP_REFERER': 'https://example.com/',
            },
            base_url='https://localhost/',
        )
        assert response.status_code == 400
        assert "not match" in to_unicode(response.data)

        response = self.client.post(
            "/",
            data={"name": "danny"},
            headers={
                'X-CSRFToken': csrf_token,
            },
            environ_base={
                'HTTP_REFERER': 'http://localhost/',
            },
            base_url='https://localhost/',
        )
        assert response.status_code == 400
        assert "not match" in to_unicode(response.data)

        response = self.client.post(
            "/",
            data={"name": "danny"},
            headers={
                'X-CSRFToken': csrf_token,
            },
            environ_base={
                'HTTP_REFERER': 'https://localhost:3000/',
            },
            base_url='https://localhost/',
        )
        assert response.status_code == 400
        assert "not match" in to_unicode(response.data)

    def test_valid_secure_csrf(self):
        response = self.client.get("/", base_url='https://localhost/')
        csrf_token = get_csrf_token(response.data)
        response = self.client.post(
            "/",
            data={"name": "danny"},
            headers={
                'X-CSRFToken': csrf_token,
            },
            environ_base={
                'HTTP_REFERER': 'https://localhost/',
            },
            base_url='https://localhost/',
        )
        assert response.status_code == 200

    def test_not_endpoint(self):
        response = self.client.post('/not-endpoint')
        assert response.status_code == 404

    def test_testing(self):
        self.app.testing = True
        self.client.post("/", data={"name": "danny"})

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
