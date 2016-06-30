from __future__ import with_statement

from .base import TestCase
from flask import json
from flask import Flask, render_template
from flask_wtf import FlaskForm
from flask_wtf.recaptcha import RecaptchaField


RECAPTCHA_PUBLIC_KEY = '6LeYIbsSAAAAACRPIllxA7wvXjIE411PfdB2gt2J'
RECAPTCHA_PRIVATE_KEY = '6LeYIbsSAAAAAJezaIq3Ft_hSTo0YtyeFG-JgRtu'


class RecaptchaFrom(FlaskForm):
    SECRET_KEY = "a poorly kept secret."
    recaptcha = RecaptchaField()


class TestRecaptcha(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.secret_key = "secret"
        app.config['RECAPTCHA_PUBLIC_KEY'] = RECAPTCHA_PUBLIC_KEY
        app.config['RECAPTCHA_PRIVATE_KEY'] = RECAPTCHA_PRIVATE_KEY

        @app.route("/", methods=("GET", "POST"))
        def index():
            form = RecaptchaFrom(csrf_enabled=False)
            if form.validate_on_submit():
                return 'OK'
            return render_template("recaptcha.html", form=form)
        return app

    def test_recaptcha(self):
        response = self.client.get('/')
        assert b'//www.google.com/recaptcha/api.js' in response.data

    def test_invalid_recaptcha(self):
        response = self.client.post('/', data={})
        assert b'missing' in response.data

    def test_send_recaptcha_request(self):
        response = self.client.post('/', data={
            'g-recaptcha-response': 'test'
        })
        assert b'invalid' in response.data

        response = self.client.post('/', data=json.dumps({
            'g-recaptcha-response': 'test'
        }), content_type='application/json')
        assert b'invalid' in response.data

    def test_testing(self):
        self.app.testing = True
        response = self.client.post('/', data={
            'g-recaptcha-response': 'test'
        })
        assert b'invalid' not in response.data

    def test_no_private_key(self):
        self.app.testing = False
        self.app.config.pop('RECAPTCHA_PRIVATE_KEY', None)
        response = self.client.post('/', data={
            'g-recaptcha-response': 'test'
        })
        assert response.status_code == 500

    def test_no_public_key(self):
        self.app.config.pop('RECAPTCHA_PUBLIC_KEY', None)
        response = self.client.get('/')
        assert response.status_code == 500
