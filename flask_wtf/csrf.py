# coding: utf-8
"""
    flask_wtf.csrf
    ~~~~~~~~~~~~~~

    CSRF protection for Flask.

    :copyright: (c) 2013 by Hsiaoming Yang.
"""

import os
import hmac
import hashlib
import time
from flask import current_app, session, request, abort
from ._compat import to_bytes


def generate_csrf(secret_key=None, time_limit=3600):
    """Generate csrf token code.

    :param secret_key: A secret key for mixing in the token,
                       default is Flask.secret_key.
    :param time_limit: Token valid in the time limit,
                       default is 3600s.
    """
    if not secret_key:
        secret_key = current_app.secret_key

    if 'csrf_token' not in session:
        session['csrf_token'] = hashlib.sha1(os.urandom(64)).hexdigest()

    if time_limit:
        expires = time.time() + time_limit
        csrf_build = '%s%s' % (session['csrf_token'], expires)
    else:
        expires = ''
        csrf_build = session['csrf_token']

    hmac_csrf = hmac.new(
        to_bytes(secret_key),
        to_bytes(csrf_build),
        digestmod=hashlib.sha1
    ).hexdigest()
    return '%s##%s' % (expires, hmac_csrf)


def validate_csrf(data, secret_key=None, time_limit=True):
    """Check if the given data is a valid csrf token.

    :param data: The csrf token value to be checked.
    :param secret_key: A secret key for mixing in the token,
                       default is Flask.secret_key.
    :param time_limit: Check if the csrf token is expired.
                       default is True.
    """
    if not data or '##' not in data:
        return False

    expires, hmac_csrf = data.split('##')
    try:
        expires = float(expires)
    except:
        return False

    if time_limit:
        now = time.time()
        if now > expires:
            return False

    if not secret_key:
        secret_key = current_app.secret_key

    csrf_build = '%s%s' % (session['csrf_token'], expires)
    hmac_compare = hmac.new(
        to_bytes(secret_key),
        to_bytes(csrf_build),
        digestmod=hashlib.sha1
    ).hexdigest()
    return hmac_compare == hmac_csrf


class CsrfProtect(object):
    """Enable csrf protect for Flask.

    Register it with::

        app = Flask(__name__)
        CsrfProtect(app)

    And in the templates, add the token input::

        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>

    If you need to send the token via AJAX, and there is no form::

        <meta name="csrf_token" value="{{ csrf_token() }}" />

    You can grab the csrf token with JavaScript, and send the token together.
    """

    def __init__(self, app=None, on_csrf=None):
        self.on_csrf = on_csrf
        self._exempt_views = set()

        if app:
            self.init_app(app)

    def init_app(self, app):
        secret_key = app.config.get('WTF_CSRF_SECRET_KEY', app.secret_key)
        app.jinja_env.globals['csrf_token'] = generate_csrf

        @app.before_request
        def _csrf_protect():
            if app.testing:
                return
            if not request.method == 'POST':
                return

            view = app.view_functions.get(request.endpoint)
            dest = '%s.%s' % (view.__module__, view.__name__)
            if self._exempt_views and dest in self._exempt_views:
                return

            request.csrf_protected = True
            csrf_token = request.form.get('csrf_token')
            if not validate_csrf(csrf_token, secret_key):
                if self.on_csrf:
                    self.on_csrf(request)
                return abort(400)

    def exempt(self, view):
        """A decorator that can exclude a view from csrf protection.

        Remember to put the decorator above the `route`::

            csrf = CsrfProtect(app)

            @csrf.exempt
            @app.route('/some-view', methods=['POST'])
            def some_view():
                return
        """
        view_location = '%s.%s' % (view.__module__, view.__name__)
        self._exempt_views.add(view_location)
        return view
