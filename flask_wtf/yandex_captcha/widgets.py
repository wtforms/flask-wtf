# -*- coding: utf-8 -*-

try:
    import urllib2 as http
except ImportError:
    # Python 3
    from urllib import request as http

import re
from flask import current_app, Markup, json
from werkzeug import url_encode
from . import YANDEX_CLEANWEB_API_URL
from .._compat import to_bytes

PATTERN_SPAM_ID = re.compile(b'<id>(.*)</id>')
PATTERN_CAPTCHA_ID = re.compile(b'<captcha>(.*)</captcha>')
PATTERN_CAPTCHA_URL = re.compile(b'<url>(.*)</url>')


YANDEX_CAPTCHA_HTML = u"""
<script type="text/javascript">var YandexCaptchaOptions = %(options)s;</script>
<script type="text/javascript" src="%(script_url)s"></script>
  <div>
    <img name="yandex_captcha_image" src="%(captcha_url)s" width="200" height="60">
    <input name="yandex_captcha_challenge_field" type="text" placeholder="%(captcha_placeholder)s" />
    <input type="hidden" name="yandex_captcha_captcha_id_field" value="%(captcha_id)s" />
    <input type="hidden" name="yandex_captcha_spam_id_field" value="%(spam_id)s" />
  </div>
"""


__all__ = ['YandexCaptchaWidget']


class YandexCaptchaWidget(object):

    def yandex_captcha_html(self, captcha_id, captcha_url, spam_id, **kwargs):
        html = current_app.config.get('YANDEX_CAPTCHA_HTML', YANDEX_CAPTCHA_HTML)
        context = dict(
            options=json.dumps(
                current_app.config.get('YANDEX_CLEANWEB_CAPTCHA_OPTIONS', {}),
                cls=json.JSONEncoder
            ),
            script_url=current_app.config.get('YANDEX_CLEANWEB_CAPTCHA_SCRIPT', ''),
            captcha_url=captcha_url,
            captcha_placeholder=current_app.config.get('YANDEX_CLEANWEB_CAPTCHA_PLACEHOLDER', ''),
            captcha_id=captcha_id,
            spam_id=spam_id
        )
        return Markup(html % context)

    def __call__(self, field, error=None, **kwargs):
        """
            Returns the YandexCaptcha input HTML.
        """

        try:
            api_key = current_app.config['YANDEX_CLEANWEB_API_KEY']
        except KeyError:
            raise RuntimeError('YANDEX_CLEANWEB_API_KEY config not set')

        data = url_encode({
            'body-plain': 'vodka nuclear balalaika',
            'key': api_key
        })

        response = http.urlopen(YANDEX_CLEANWEB_API_URL + 'check-spam', to_bytes(data))

        spam_id = PATTERN_SPAM_ID.findall(response.read())[0]

        ### getting captcha url ###

        data = url_encode({
            'id': spam_id,
            'key': api_key,
            'type': current_app.config.get('YANDEX_CLEANWEB_CAPTCHA_TYPE', 'std')
        })
        response = http.urlopen(YANDEX_CLEANWEB_API_URL + 'get-captcha', to_bytes(data))

        response = response.read()

        captcha_id = PATTERN_CAPTCHA_ID.findall(response)[0]
        captcha_url = PATTERN_CAPTCHA_URL.findall(response)[0]

        return self.yandex_captcha_html(captcha_id, captcha_url, spam_id)
