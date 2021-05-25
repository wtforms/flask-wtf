from flask import Markup, current_app, json
from werkzeug.urls import url_encode

JSONEncoder = json.JSONEncoder

RECAPTCHA_SCRIPT = 'https://www.google.com/recaptcha/api.js'
RECAPTCHA_TEMPLATE = '''
<script src='%s' async defer></script>
<div class="g-recaptcha" %s></div>
'''

__all__ = ['RecaptchaWidget']


class RecaptchaWidget:

    def recaptcha_html(self, public_key):
        html = current_app.config.get('RECAPTCHA_HTML')
        if html:
            return Markup(html)
        params = current_app.config.get('RECAPTCHA_PARAMETERS')
        script = RECAPTCHA_SCRIPT
        if params:
            script += '?' + url_encode(params)

        attrs = current_app.config.get('RECAPTCHA_DATA_ATTRS', {})
        attrs['sitekey'] = public_key
        snippet = ' '.join(['data-{}="{}"'.format(k, attrs[k]) for k in attrs])
        return Markup(RECAPTCHA_TEMPLATE % (script, snippet))

    def __call__(self, field, error=None, **kwargs):
        """Returns the recaptcha input HTML."""

        try:
            public_key = current_app.config['RECAPTCHA_PUBLIC_KEY']
        except KeyError:
            raise RuntimeError('RECAPTCHA_PUBLIC_KEY config not set')

        return self.recaptcha_html(public_key)
