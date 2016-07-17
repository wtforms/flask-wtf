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
            return request.accept_languages.best_match(
                ['en', 'ru'], default='en')

        response = self.client.post(
            "/",
            headers=[("Accept-Language", "ru")],
            data={}
        )
        # Russian for 'This field is required':
        assert '\u0414\u0430\u043d\u043d\u043e\u0435 ' \
               '\u043f\u043e\u043b\u0435 ' \
               '\u043e\u0431\u044f\u0437\u0430\u0442\u0435\u043b\u044c\u043d\u043e' \
               in to_unicode(response.data)

        # If no `Accept-Language` is sent, use default (`en`):
        response = self.client.post("/", data={})
        assert b'This field is required.' in response.data
