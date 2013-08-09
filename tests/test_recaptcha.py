from __future__ import with_statement

from .base import TestCase, to_unicode
from flask import Flask, render_template
from flask_wtf import Form
from flask_wtf.recaptcha import RecaptchaField


RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'


class RecaptchaFrom(Form):
    SECRET_KEY = "a poorly kept secret."
    recaptcha = RecaptchaField()


class TestRecaptcha(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.secret_key = "secret"
        app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY
        app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY

        @app.route("/", methods=("GET", "POST"))
        def inex():
            form = RecaptchaFrom(csrf_enabled=False)
            if form.validate_on_submit():
                return 'OK'
            return render_template("recaptcha.html", form=form)
        return app

    def test_recaptcha(self):
        response = self.client.get('/')
        assert 'http://api.recaptcha.net' in to_unicode(response.data)

    def test_ssl_recaptcha(self):
        self.app.config['RECAPTCHA_USE_SSL'] = True
        response = self.client.get('/')
        ret = to_unicode(response.data)
        assert 'https://www.google.com/recaptcha/api/' in ret

    def test_invalid_recaptcha(self):
        response = self.client.post('/', data={})
        assert 'Invalid word' in to_unicode(response.data)

    def test_send_recaptcha_request(self):
        response = self.client.post('/', data={
            'recaptcha_challenge_field': 'test',
            'recaptcha_response_field': 'test'
        })
        assert 'Invalid word' in to_unicode(response.data)

    def test_testing(self):
        self.app.testing = True
        response = self.client.post('/', data={
            'recaptcha_challenge_field': 'test',
            'recaptcha_response_field': 'test'
        })
        assert 'Invalid word' not in to_unicode(response.data)

    def test_no_private_key(self):
        self.app.config.pop('RECAPTCHA_PRIVATE_KEY', None)
        response = self.client.post('/', data={
            'recaptcha_challenge_field': 'test',
            'recaptcha_response_field': 'test'
        })
        assert response.status_code == 500

    def test_no_public_key(self):
        self.app.config.pop('RECAPTCHA_PUBLIC_KEY', None)
        response = self.client.get('/')
        assert response.status_code == 500
