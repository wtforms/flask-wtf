from __future__ import with_statement

from .base import TestCase, to_unicode


class TestI18NCase(TestCase):
    def test_i18n_disabled(self):
        self.app.config['CSRF_ENABLED'] = False
        response = self.client.post(
            "/",
            headers={'Accept-Language': 'zh-CN,zh;q=0.8'},
            data={}
        )
        assert b'This field is required.' in response.data

    def test_i18n_enabled(self):
        from flask import request
        from flask_babel import Babel
        babel = Babel(self.app)

        @babel.localeselector
        def get_locale():
            return request.accept_languages.best_match(['en', 'zh'], 'en')

        self.app.config['CSRF_ENABLED'] = False

        response = self.client.post(
            "/",
            headers={'Accept-Language': 'zh-CN,zh;q=0.8'},
            data={}
        )
        assert '\u8be5\u5b57\u6bb5\u662f' in to_unicode(response.data)

        response = self.client.post("/", data={})
        assert b'This field is required.' in response.data
