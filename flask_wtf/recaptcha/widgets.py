# -*- coding: utf-8 -*-

from flask import current_app, Markup
from werkzeug import url_encode
from flask import json
from .._compat import text_type
JSONEncoder = json.JSONEncoder

try:
    from speaklater import _LazyString

    class _JSONEncoder(JSONEncoder):
        def default(self, o):
            if isinstance(o, _LazyString):
                return str(o)
            return JSONEncoder.default(self, o)
except ImportError:
    _JSONEncoder = JSONEncoder


RECAPTCHA_API_SERVER = '//www.google.com/recaptcha/api/'
RECAPTCHA_HTML = u'''
<script type="text/javascript">var RecaptchaOptions = %(options)s;</script>
<script type="text/javascript" src="%(script_url)s"></script>
<noscript>
  <iframe src="%(frame_url)s" height="300" width="500" frameborder="0"></iframe><br>
  <textarea name="recaptcha_challenge_field" rows="3" cols="40"></textarea>
  <input type="hidden" name="recaptcha_response_field" value="manual_challenge">
</noscript>
'''

__all__ = ["RecaptchaWidget"]


class RecaptchaWidget(object):

    def recaptcha_html(self, query, options):
        html = current_app.config.get('RECAPTCHA_HTML', RECAPTCHA_HTML)
        server = current_app.config.get(
            'RECAPTCHA_API_SERVER', RECAPTCHA_API_SERVER
        )
        return Markup(html % dict(
            script_url='%schallenge?%s' % (server, query),
            frame_url='%snoscript?%s' % (server, query),
            options=json.dumps(options, cls=_JSONEncoder)
        ))

    def __call__(self, field, error=None, **kwargs):
        """Returns the recaptcha input HTML."""

        try:
            public_key = current_app.config['RECAPTCHA_PUBLIC_KEY']
        except KeyError:
            raise RuntimeError("RECAPTCHA_PUBLIC_KEY config not set")
        query_options = dict(k=public_key)

        if field.recaptcha_error is not None:
            query_options['error'] = text_type(field.recaptcha_error)

        query = url_encode(query_options)

        _ = field.gettext

        options = {
            'theme': 'clean',
            'custom_translations': {
                'audio_challenge': _('Get an audio challenge'),
                'cant_hear_this': _('Download sound as MP3'),
                'help_btn': _('Help'),
                'image_alt_text': _('reCAPTCHA challenge image'),
                'incorrect_try_again': _('Incorrect. Try again.'),
                'instructions_audio': _('Type what you hear'),
                'instructions_visual': _('Type the text'),
                'play_again': _('Play sound again'),
                'privacy_and_terms': _('Privacy & Terms'),
                'refresh_btn': _('Get a new challenge'),
                'visual_challenge': _('Get a visual challenge'),
            }
        }

        options.update(current_app.config.get('RECAPTCHA_OPTIONS', {}))

        return self.recaptcha_html(query, options)
