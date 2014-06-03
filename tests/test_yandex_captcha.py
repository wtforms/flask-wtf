from __future__ import with_statement

from .base import TestCase
from flask import Flask, render_template
from flask_wtf import Form
from flask_wtf.yandex_captcha import YandexCaptchaField


YANDEX_CLEANWEB_API_PUBLIC_KEY = 'cw.1.1.20110707T172051Z.faf547ce44f3d10b.d7e3028845ea04f56c38f7eef90999f765dd0d1f'


class YandexCaptchaForm(Form):
    SECRET_KEY = 'a poorly kept secret.'
    yandex_captcha = YandexCaptchaField()


class TestYandexCaptcha(TestCase):
    def create_app(self):
        app = Flask(__name__)
        app.secret_key = 'secret'
        app.config['YANDEX_CLEANWEB_API_KEY'] = YANDEX_CLEANWEB_API_PUBLIC_KEY

        @app.route("/", methods=("GET", "POST"))
        def index():
            form = YandexCaptchaForm(csrf_enabled=False)
            if form.validate_on_submit():
                return 'OK'
            return render_template('yandex_captcha.html', form=form)
        return app

    def test_yandex_captcha(self):
        response = self.client.get('/')
        assert 'yandex_captcha_image' in response.data

    def test_invalid_yandex_captcha(self):
        response = self.client.post('/', data={})
        assert 'Invalid code' in response.data

    def test_send_yandex_captcha_request(self):
        response = self.client.post('/', data={
            'yandex_captcha_challenge_field': 'wrong data',
            'yandex_captcha_response_field': 'wrong data'
        })
        assert 'Invalid code' in response.data

    def test_testing(self):
        self.app.testing = True
        response = self.client.post('/', data={
            'yandex_captcha_challenge_field': 'test',
            'yandex_captcha_response_field': 'test'
        })
        assert 'OK' in response.data

    def test_no_api_key(self):
        self.app.config.pop('YANDEX_CLEANWEB_API_KEY', None)
        response = self.client.post('/', data={
            'yandex_captcha_challenge_field': 'test',
            'yandex_captcha_response_field': 'test'
        })
        assert response.status_code == 500