# -*- coding: utf-8 -*-

from flask import Markup, current_app, json
from werkzeug import url_encode

JSONEncoder = json.JSONEncoder

RECAPTCHA_SCRIPT = u'https://www.google.com/recaptcha/api.js'
RECAPTCHA_NONCE = u' nonce="%s"'
RECAPTCHA_TEMPLATE = u'''
<script src='%s' async defer%s></script>
<div class="g-recaptcha" %s></div>
'''

__all__ = ['RecaptchaWidget']


class RecaptchaWidget(object):

    def recaptcha_html(self, public_key, nonce=None):
        html = current_app.config.get('RECAPTCHA_HTML')
        if html:
            return Markup(html)
        params = current_app.config.get('RECAPTCHA_PARAMETERS')
        script = RECAPTCHA_SCRIPT
        if params:
            script += u'?' + url_encode(params)

        nonce_attr = ''
        if nonce is not None:
            nonce_attr = RECAPTCHA_NONCE % nonce

        attrs = current_app.config.get('RECAPTCHA_DATA_ATTRS', {})
        attrs['sitekey'] = public_key
        snippet = u' '.join([u'data-%s="%s"' % (k, attrs[k]) for k in attrs])
        return Markup(RECAPTCHA_TEMPLATE % (script, nonce_attr, snippet))

    def __call__(self, field, error=None, **kwargs):
        """Returns the recaptcha input HTML."""

        try:
            public_key = current_app.config['RECAPTCHA_PUBLIC_KEY']
        except KeyError:
            raise RuntimeError('RECAPTCHA_PUBLIC_KEY config not set')

        return self.recaptcha_html(public_key, nonce=field.nonce)
