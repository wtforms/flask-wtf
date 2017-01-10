from __future__ import with_statement

import re
import warnings

from flask import Blueprint, abort, render_template, request
from flask import g
from wtforms import ValidationError

from flask_wtf._compat import FlaskWTFDeprecationWarning
from flask_wtf.csrf import CSRFError, CSRFProtect, generate_csrf, validate_csrf
from .base import MyForm, TestCase


class TestCSRF(TestCase):
    def setUp(self):
        app = self.create_app()
        app.config['WTF_CSRF_SECRET_KEY'] = "a poorly kept secret."
        csrf = CSRFProtect(app)
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

        @csrf.exempt
        @app.route('/csrf-protect-method', methods=['GET', 'POST'])
        def csrf_protect_method():
            csrf.protect()
            return 'protected'

        bp = Blueprint('csrf', __name__)

        @bp.route('/foo', methods=['GET', 'POST'])
        def foo():
            return 'foo'

        app.register_blueprint(bp, url_prefix='/bar')
        self.bp = bp
        self.app = app
        self.client = self.app.test_client()

    def test_invalid_csrf(self):
        response = self.client.post("/", data={"name": "danny"})
        assert response.status_code == 400

        @self.app.errorhandler(CSRFError)
        def handle_csrf_error(e):
            return e, 200

        response = self.client.post("/", data={"name": "danny"})
        assert response.status_code == 200
        assert b'The CSRF token is missing.' in response.data

    def test_invalid_csrf2(self):
        # tests with bad token
        response = self.client.post("/", data={
            "name": "danny",
            "csrf_token": "9999999999999##test"
            # will work only if greater than time.time()
        })
        assert response.status_code == 400

    def test_invalid_secure_csrf3(self):
        # test with multiple separators
        response = self.client.post("/", data={
            "name": "danny",
            "csrf_token": "1378915137.722##foo##bar##and"
            # will work only if greater than time.time()
        })
        assert response.status_code == 400

    def test_valid_csrf(self):
        with self.client:
            self.client.get('/')
            csrf_token = g.csrf_token

        response = self.client.post("/", data={
            "name": "danny",
            "csrf_token": csrf_token
        })
        assert b'DANNY' in response.data

    def test_prefixed_csrf(self):
        with self.client:
            self.client.get('/')
            csrf_token = g.csrf_token

        response = self.client.post('/', data={
            'prefix-name': 'David',
            'prefix-csrf_token': csrf_token,
        })
        assert response.status_code == 200

    def test_invalid_secure_csrf(self):
        with self.client:
            self.client.get('/', base_url='https://localhost/')
            csrf_token = g.csrf_token

        response = self.client.post(
            "/",
            data={"name": "danny"},
            headers={'X-CSRFToken': csrf_token},
            base_url='https://localhost/',
        )
        assert response.status_code == 400
        assert b'The referrer header is missing.' in response.data

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
        assert b'The referrer does not match the host.' in response.data

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
        assert b'The referrer does not match the host.' in response.data

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
        assert b'The referrer does not match the host.' in response.data

    def test_valid_secure_csrf(self):
        with self.client:
            self.client.get('/', base_url='https://localhost/')
            csrf_token = g.csrf_token

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

    def test_valid_csrf_method(self):
        with self.client:
            self.client.get('/')
            csrf_token = g.csrf_token

        response = self.client.post("/csrf-protect-method", data={
            "csrf_token": csrf_token
        })
        assert response.status_code == 200

    def test_empty_csrf_headers(self):
        with self.client:
            self.client.get('/', base_url='https://localhost/')
            csrf_token = g.csrf_token

        self.app.config['WTF_CSRF_HEADERS'] = list()
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
        assert response.status_code == 400

    def test_custom_csrf_headers(self):
        with self.client:
            self.client.get('/', base_url='https://localhost/')
            csrf_token = g.csrf_token

        self.app.config['WTF_CSRF_HEADERS'] = ['X-XSRF-TOKEN']
        response = self.client.post(
            "/",
            data={"name": "danny"},
            headers={
                'X-XSRF-TOKEN': csrf_token,
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

    def test_csrf_exempt_view_with_form(self):
        with self.client:
            self.client.get('/', base_url='https://localhost/')
            csrf_token = g.csrf_token

        response = self.client.post("/csrf-exempt", data={
            "name": "danny",
            "csrf_token": csrf_token
        })
        assert b'DANNY' in response.data

    def test_validate_csrf(self):
        with self.app.test_request_context():
            self.assertRaises(ValidationError, validate_csrf, None)
            self.assertRaises(ValidationError, validate_csrf, 'invalid')
            validate_csrf(generate_csrf())

    def test_validate_not_expiring_csrf(self):
        with self.app.test_request_context():
            csrf_token = generate_csrf()
            validate_csrf(csrf_token, time_limit=False)

    def test_csrf_token_helper(self):
        @self.app.route("/token")
        def withtoken():
            return render_template("csrf.html")

        with self.client:
            response = self.client.get('/token')
            assert re.search(br'token: ([0-9a-zA-Z\-._]+)', response.data)

    def test_csrf_blueprint(self):
        response = self.client.post('/bar/foo')
        assert response.status_code == 400

        self.csrf.exempt(self.bp)
        response = self.client.post('/bar/foo')
        assert response.status_code == 200

    def test_csrf_token_macro(self):
        @self.app.route("/token")
        def withtoken():
            return render_template("import_csrf.html")

        with self.client:
            response = self.client.get('/token')
            assert g.csrf_token in response.data.decode('utf8')

    def test_csrf_custom_token_key(self):
        with self.app.test_request_context():
            # Generate a normal and a custom CSRF token
            default_csrf_token = generate_csrf()
            custom_csrf_token = generate_csrf(token_key='oauth_state')

            # Verify they are different due to using different session keys
            self.assertNotEqual(default_csrf_token, custom_csrf_token)

            # However, the custom key can validate as well
            validate_csrf(custom_csrf_token, token_key='oauth_state')

    def test_old_error_handler(self):
        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always', FlaskWTFDeprecationWarning)

            @self.csrf.error_handler
            def handle_csrf_error(reason):
                return 'caught csrf return'

            self.assertEqual(len(w), 1)
            assert issubclass(w[0].category, FlaskWTFDeprecationWarning)
            assert 'app.errorhandler(CSRFError)' in str(w[0].message)

            rv = self.client.post('/', data={'name': 'david'})
            assert b'caught csrf return' in rv.data

        with warnings.catch_warnings(record=True) as w:
            warnings.simplefilter('always', FlaskWTFDeprecationWarning)

            @self.csrf.error_handler
            def handle_csrf_error(reason):
                abort(401, 'caught csrf abort')

            self.assertEqual(len(w), 1)
            assert issubclass(w[0].category, FlaskWTFDeprecationWarning)
            assert 'app.errorhandler(CSRFError)' in str(w[0].message)

            rv = self.client.post('/', data={'name': 'david'})
            assert b'caught csrf abort' in rv.data
