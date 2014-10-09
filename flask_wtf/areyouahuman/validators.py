# -*- coding: utf-8 -*-

try:
    import urllib2 as http
except ImportError:
    # Python 3
    from urllib import request as http

from flask import request, current_app, json
from wtforms import ValidationError
from werkzeug import url_encode

__all__ = ["AreYouAHuman"]


class AreYouAHuman(object):
    """Validates an are You a Human ?"""

    def __init__(self, message=u'Invalid game score. Please try again.'):
        self.message = message

    def __call__(self, form, field):
        config = current_app.config
        if current_app.testing and 'WTF_AYAH_PUBLISHER_KEY' not in config:
            return True

        challenge = request.form.get('session_secret', '')
        remote_ip = request.remote_addr

        if not challenge:
            raise ValidationError(field.gettext(self.message))

        if not self._validate_areyouahuman(challenge, remote_ip):
            raise ValidationError(field.gettext(self.message))

    def _validate_areyouahuman(self, challenge, remote_addr):
        config = current_app.config
        server = config.get('WTF_AYAH_SERVER', 'ws.areyouahuman.com')
        data = {'scoring_key': config['WTF_AYAH_SCORING_KEY'],
                'session_secret': challenge}
        scoring_url = "https://{}/ws/scoreGame".format(server)
        values = url_encode(data)
        response = http.urlopen(scoring_url, values)
        result = False
        if response.code == 200:
            content = json.loads(response.readline())
            result = content['status_code']
        return result
