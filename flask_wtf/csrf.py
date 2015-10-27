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
from flask import Blueprint
from flask import current_app, session, request, abort
from werkzeug.security import safe_str_cmp
from ._compat import to_bytes, string_types
try:
    from urlparse import urlparse
except ImportError:
    # python 3
    from urllib.parse import urlparse


__all__ = ('generate_csrf', 'validate_csrf', 'CsrfProtect')


def generate_csrf(secret_key=None, time_limit=None, token_key='csrf_token', url_safe=False):
    """Generate csrf token code.

    :param secret_key: A secret key for mixing in the token,
                       default is Flask.secret_key.
    :param time_limit: Token valid in the time limit,
                       default is 3600s.
    """
    if not secret_key:
        secret_key = current_app.config.get(
            'WTF_CSRF_SECRET_KEY', current_app.secret_key
        )

    if not secret_key:
        raise Exception('Must provide secret_key to use csrf.')

    if time_limit is None:
        time_limit = current_app.config.get('WTF_CSRF_TIME_LIMIT', 3600)

    if token_key not in session:
        session[token_key] = hashlib.sha1(os.urandom(64)).hexdigest()

    if time_limit:
        expires = int(time.time() + time_limit)
        csrf_build = '%s%s' % (session[token_key], expires)
    else:
        expires = ''
        csrf_build = session[token_key]

    hmac_csrf = hmac.new(
        to_bytes(secret_key),
        to_bytes(csrf_build),
        digestmod=hashlib.sha1
    ).hexdigest()
    delimiter = '--' if url_safe else '##'
    return '%s%s%s' % (expires, delimiter, hmac_csrf)


def validate_csrf(data, secret_key=None, time_limit=None, token_key='csrf_token', url_safe=False):
    """Check if the given data is a valid csrf token.

    :param data: The csrf token value to be checked.
    :param secret_key: A secret key for mixing in the token,
                       default is Flask.secret_key.
    :param time_limit: Check if the csrf token is expired.
                       default is True.
    """
    delimiter = '--' if url_safe else '##'
    if not data or delimiter not in data:
        return False

    try:
        expires, hmac_csrf = data.split(delimiter, 1)
    except ValueError:
        return False  # unpack error

    if time_limit is None:
        time_limit = current_app.config.get('WTF_CSRF_TIME_LIMIT', 3600)

    if time_limit:
        try:
            expires = int(expires)
        except ValueError:
            return False

        now = int(time.time())
        if now > expires:
            return False

    if not secret_key:
        secret_key = current_app.config.get(
            'WTF_CSRF_SECRET_KEY', current_app.secret_key
        )

    if token_key not in session:
        return False

    csrf_build = '%s%s' % (session[token_key], expires)
    hmac_compare = hmac.new(
        to_bytes(secret_key),
        to_bytes(csrf_build),
        digestmod=hashlib.sha1
    ).hexdigest()

    return safe_str_cmp(hmac_compare, hmac_csrf)


class CsrfProtect(object):
    """Enable csrf protect for Flask.

    Register it with::

        app = Flask(__name__)
        CsrfProtect(app)

    And in the templates, add the token input::

        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>

    If you need to send the token via AJAX, and there is no form::

        <meta name="csrf_token" content="{{ csrf_token() }}" />

    You can grab the csrf token with JavaScript, and send the token together.
    """

    def __init__(self, app=None):
        self._exempt_views = set()
        self._exempt_blueprints = set()

        if app:
            self.init_app(app)

    def init_app(self, app):
        self._app = app
        app.jinja_env.globals['csrf_token'] = generate_csrf
        app.config.setdefault(
            'WTF_CSRF_HEADERS', ['X-CSRFToken', 'X-CSRF-Token']
        )
        app.config.setdefault('WTF_CSRF_SSL_STRICT', True)
        app.config.setdefault('WTF_CSRF_ENABLED', True)
        app.config.setdefault('WTF_CSRF_CHECK_DEFAULT', True)
        app.config.setdefault('WTF_CSRF_METHODS', ['POST', 'PUT', 'PATCH'])

        # expose csrf_token as a helper in all templates
        @app.context_processor
        def csrf_token():
            return dict(csrf_token=generate_csrf)

        @app.before_request
        def _csrf_protect():
            # many things come from django.middleware.csrf
            if not app.config['WTF_CSRF_ENABLED']:
                return

            if not app.config['WTF_CSRF_CHECK_DEFAULT']:
                return

            if request.method not in app.config['WTF_CSRF_METHODS']:
                return

            if self._exempt_views or self._exempt_blueprints:
                if not request.endpoint:
                    return

                view = app.view_functions.get(request.endpoint)
                if not view:
                    return

                dest = '%s.%s' % (view.__module__, view.__name__)
                if dest in self._exempt_views:
                    return
                if request.blueprint in self._exempt_blueprints:
                    return

            self.protect()

    def _get_csrf_token(self):
        # find the ``csrf_token`` field in the subitted form
        # if the form had a prefix, the name will be
        # ``{prefix}-csrf_token``
        for key in request.form:
            if key.endswith('csrf_token'):
                csrf_token = request.form[key]
                if csrf_token:
                    return csrf_token

        for header_name in self._app.config['WTF_CSRF_HEADERS']:
            csrf_token = request.headers.get(header_name)
            if csrf_token:
                return csrf_token
        return None

    def protect(self):
        if request.method not in self._app.config['WTF_CSRF_METHODS']:
            return

        if not validate_csrf(self._get_csrf_token()):
            reason = 'CSRF token missing or incorrect.'
            return self._error_response(reason)

        if request.is_secure and self._app.config['WTF_CSRF_SSL_STRICT']:
            if not request.referrer:
                reason = 'Referrer checking failed - no Referrer.'
                return self._error_response(reason)

            good_referrer = 'https://%s/' % request.host
            if not same_origin(request.referrer, good_referrer):
                reason = 'Referrer checking failed - origin does not match.'
                return self._error_response(reason)

        request.csrf_valid = True  # mark this request is csrf valid

    def exempt(self, view):
        """A decorator that can exclude a view from csrf protection.

        Remember to put the decorator above the `route`::

            csrf = CsrfProtect(app)

            @csrf.exempt
            @app.route('/some-view', methods=['POST'])
            def some_view():
                return
        """
        if isinstance(view, Blueprint):
            self._exempt_blueprints.add(view.name)
            return view
        if isinstance(view, string_types):
            view_location = view
        else:
            view_location = '%s.%s' % (view.__module__, view.__name__)
        self._exempt_views.add(view_location)
        return view

    def _error_response(self, reason):
        return abort(400, reason)

    def error_handler(self, view):
        """A decorator that set the error response handler.

        It accepts one parameter `reason`::

            @csrf.error_handler
            def csrf_error(reason):
                return render_template('error.html', reason=reason)

        By default, it will return a 400 response.
        """
        self._error_response = view
        return view


def same_origin(current_uri, compare_uri):
    parsed_uri = urlparse(current_uri)
    parsed_compare = urlparse(compare_uri)

    if parsed_uri.scheme != parsed_compare.scheme:
        return False

    if parsed_uri.hostname != parsed_compare.hostname:
        return False

    if parsed_uri.port != parsed_compare.port:
        return False
    return True
