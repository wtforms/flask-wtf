# -*- coding: utf-8 -*-

from flask import current_app, Markup
from werkzeug import url_encode, url_quote
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
except:
    _JSONEncoder = JSONEncoder

__all__ = ["AreYouAHumanWidget"]


class AreYouAHumanWidget(object):

    def areyouahuman_html(self, server, query, html):
        return Markup(html % dict(
            script_url='%schallenge?%s' % (server, query),
            frame_url='%snoscript?%s' % (server, query)
        ))

    def __call__(self, field, error=None, **kwargs):
        """Returns the areyouahuman input HTML."""

        current_app.config.setdefault('WTF_AYAH_SERVER', 'ws.areyouahuman.com')
        try:
            public_key = current_app.config['WTF_AYAH_PUBLISHER_KEY']
        except KeyError:
            raise RuntimeError("AYAH_PUBLISHER_KEY/AYAH_SCORING_KEY \
                                config not set")
        query_options = dict(k=public_key)

        if field.areyouahuman_error is not None:
            query_options['error'] = text_type(field.areyouahuman_error)

        query = url_encode(query_options)

        server = current_app.config['WTF_AYAH_SERVER']
        publisher_url = ''.join(['https://', server, '/ws/script/',
                                url_quote(public_key, safe='')])
        publisher_html = u''.join(['<div id="AYAH"></div> \
                                     <script type="text/javascript" \
                                             src="', publisher_url, '"> \
                                     </script>'])

        return self.areyouahuman_html(server, query, publisher_html)
