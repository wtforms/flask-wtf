try:
    import urllib2 as http
except ImportError:
    # Python 3
    from urllib import request as http

from bs4 import BeautifulSoup
from flask import request, current_app
from wtforms import ValidationError
from werkzeug import url_encode

from . import YANDEX_CLEANWEB_API_URL
from .._compat import to_bytes

__all__ = ['YandexCaptcha']


class YandexCaptcha(object):
    """
        Validates a YandexCaptcha.
    """

    def __init__(self, message=u'Invalid code. Please try again.'):
        self.message = message

    def __call__(self, form, field):
        if current_app.testing:
            return True

        data_provider = request.json if request.json else request.form
        spam_id = data_provider.get('yandex_captcha_spam_id_field', '')
        captcha_id = data_provider.get('yandex_captcha_captcha_id_field', '')
        response = data_provider.get('yandex_captcha_challenge_field', '')

        if not all((spam_id, captcha_id, response)):
            raise ValidationError(field.gettext(self.message))

        if not self._validate_yandex_captcha(response, captcha_id, spam_id):
            field.yandex_captcha_error = 'incorrect-captcha-sol'
            raise ValidationError(field.gettext(self.message))

    def _validate_yandex_captcha(self, response, captcha_id, spam_id):
        """
            Performs the actual validation.
        """
        try:
            api_key = current_app.config['YANDEX_CLEANWEB_API_KEY']
        except KeyError:
            raise RuntimeError('No YANDEX_CLEANWEB_API_KEY config set')

        data = url_encode({
            'captcha': captcha_id,
            'id': spam_id,
            'value': response,
            'key': api_key
        })

        response = http.urlopen(
            YANDEX_CLEANWEB_API_URL + 'check-captcha',
            to_bytes(data)
        )

        if response.code != 200:
            if response.code in (403, 500):
                soup = BeautifulSoup(response.read())

                raise RuntimeError(
                    (
                        u'An error occurred during the request to Yandex '
                        u'CleanWeb API (%s, %s)'
                    ) % (
                        soup.error.attrs['key'],
                        soup.error.message.get_text()
                    )
                )
            raise RuntimeError()

        if BeautifulSoup(response.read()).find(
                'check-captcha-result'
        ).find('failed'):
            return False

        return True
