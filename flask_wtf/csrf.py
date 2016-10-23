# coding: utf-8
"""
    flask_wtf.csrf
    ~~~~~~~~~~~~~~

    CSRF protection for Flask.

    :copyright: (c) 2013 by Hsiaoming Yang.
"""

import hashlib
import os
import warnings
from functools import wraps

from flask import Blueprint, current_app, request, session
from itsdangerous import BadData, URLSafeTimedSerializer
from werkzeug.exceptions import BadRequest
from werkzeug.security import safe_str_cmp

from ._compat import FlaskWTFDeprecationWarning, string_types, urlparse

__all__ = ('generate_csrf', 'validate_csrf', 'CsrfProtect')


def _get_secret_key(secret_key=None):
    if not secret_key:
        secret_key = current_app.config.get('WTF_CSRF_SECRET_KEY', current_app.secret_key)

    if not secret_key:
        raise Exception('Must provide secret_key to use CSRF.')

    return secret_key


def generate_csrf(secret_key=None, token_key='csrf_token'):
    """Generate CSRF token code.

    :param secret_key: A secret key for mixing in the token, default is ``Flask.secret_key``.
    """

    if not hasattr(request, 'csrf_token'):
        if token_key not in session:
            session[token_key] = hashlib.sha1(os.urandom(64)).hexdigest()

        s = URLSafeTimedSerializer(_get_secret_key(secret_key), salt='wtf-csrf-token')
        request.csrf_token = s.dumps(session[token_key])

    return request.csrf_token


def validate_csrf(data, secret_key=None, time_limit=None, token_key='csrf_token'):
    """Check if the given data is a valid CSRF token.

    :param data: The csrf token value to be checked.
    :param secret_key: A secret key for mixing in the token,
                       default is Flask.secret_key.
    :param time_limit: Check if the csrf token is expired.
                       default is True.
    """

    if not data or token_key not in session:
        return False

    s = URLSafeTimedSerializer(_get_secret_key(secret_key), salt='wtf-csrf-token')

    if time_limit is None:
        time_limit = current_app.config.get('WTF_CSRF_TIME_LIMIT', 3600)

    try:
        token = s.loads(data, max_age=time_limit)
    except BadData:
        return False

    return safe_str_cmp(session[token_key], token)


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
        app.config.setdefault('WTF_CSRF_ENABLED', True)
        app.config.setdefault('WTF_CSRF_CHECK_DEFAULT', True)
        app.config['WTF_CSRF_METHODS'] = set(app.config.get(
            'WTF_CSRF_METHODS', ['POST', 'PUT', 'PATCH', 'DELETE']
        ))
        app.config.setdefault('WTF_CSRF_HEADERS', ['X-CSRFToken', 'X-CSRF-Token'])
        app.config.setdefault('WTF_CSRF_SSL_STRICT', True)

        app.jinja_env.globals['csrf_token'] = generate_csrf
        app.context_processor(lambda: {'csrf_token': generate_csrf})

        @app.before_request
        def _csrf_protect():
            # many things come from django.middleware.csrf
            if not app.config['WTF_CSRF_ENABLED']:
                return

            if not app.config['WTF_CSRF_CHECK_DEFAULT']:
                return

            if request.method not in app.config['WTF_CSRF_METHODS']:
                return

            if not request.endpoint:
                return

            view = app.view_functions.get(request.endpoint)

            if not view:
                return

            if request.blueprint in self._exempt_blueprints:
                return

            dest = '%s.%s' % (view.__module__, view.__name__)

            if dest in self._exempt_views:
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

        for header_name in current_app.config['WTF_CSRF_HEADERS']:
            csrf_token = request.headers.get(header_name)

            if csrf_token:
                return csrf_token

        return None

    def protect(self):
        if request.method not in current_app.config['WTF_CSRF_METHODS']:
            return

        if not validate_csrf(self._get_csrf_token()):
            self._error_response('CSRF token missing or incorrect.')

        if request.is_secure and current_app.config['WTF_CSRF_SSL_STRICT']:
            if not request.referrer:
                self._error_response('Referrer checking failed - no Referrer.')

            good_referrer = 'https://%s/' % request.host

            if not same_origin(request.referrer, good_referrer):
                self._error_response('Referrer checking failed - origin does not match.')

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
        raise CsrfError(reason)

    def error_handler(self, view):
        """A decorator that set the error response handler.

        It accepts one parameter `reason`::

            @csrf.error_handler
            def csrf_error(reason):
                return render_template('error.html', reason=reason)

        By default, it will return a 400 response.
        """

        warnings.warn(FlaskWTFDeprecationWarning(
            '"@csrf.error_handler" is deprecated. Use the standard Flask error '
            'system with "@app.errorhandler(CsrfError)" instead.'
        ), stacklevel=2)

        @wraps(view)
        def handler(reason):
            response = current_app.make_response(view(reason))
            raise CsrfError(response.get_data(as_text=True), response=response)

        self._error_response = handler
        return view


class CsrfError(BadRequest):
    description = 'CSRF token missing or incorrect.'


def same_origin(current_uri, compare_uri):
    current = urlparse(current_uri)
    compare = urlparse(compare_uri)

    return (
        current.scheme == compare.scheme
        and current.hostname == compare.hostname
        and current.port == compare.port
    )
