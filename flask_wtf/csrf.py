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
    """Generate a CSRF token. The token is cached for a request, so multiple
    calls to this function will generate the same token.

    During testing, it might be useful to access the signed token in
    ``request.csrf_token`` and the raw token in ``session['csrf_token']``.

    :param secret_key: Used to securely sign the token. Default is
        ``WTF_CSRF_SECRET_KEY`` or ``SECRET_KEY``.
    :param token_key: key where token is stored in session for comparision.
    """

    if not getattr(request, token_key, None):
        if token_key not in session:
            session[token_key] = hashlib.sha1(os.urandom(64)).hexdigest()

        s = URLSafeTimedSerializer(_get_secret_key(secret_key), salt='wtf-csrf-token')
        setattr(request, token_key, s.dumps(session[token_key]))

    return getattr(request, token_key)


def validate_csrf(data, secret_key=None, time_limit=None, token_key='csrf_token'):
    """Check if the given data is a valid CSRF token. This compares the given
    signed token to the one stored in the session.

    :param data: The signed CSRF token to be checked.
    :param secret_key: Used to securely sign the token. Default is
        ``WTF_CSRF_SECRET_KEY`` or ``SECRET_KEY``.
    :param time_limit: Number of seconds that the token is valid. Default is
        ``WTF_CSRF_TIME_LIMIT`` or 3600 seconds (60 minutes).
    :param token_key: key where token is stored in session for comparision.
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
    """Enable CSRF protection globally for a Flask app.

    ::

        app = Flask(__name__)
        csrf = CsrfProtect(app)

    Checks the ``csrf_token`` field sent with forms, or the ``X-CSRFToken``
    header sent with JavaScript requests. Render the token in templates using
    ``{{ csrf_token() }}``.

    See the :ref:`csrf` documentation.
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
        """Mark a view or blueprint to be excluded from CSRF protection.

        ::

            @app.route('/some-view', methods=['POST'])
            @csrf.exempt
            def some_view():
                ...

        ::

            bp = Blueprint(...)
            csrf.exempt(bp)

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
        """Register a function that will generate the response for CSRF errors.

        .. deprecated:: 0.14
            Use the standard Flask error system with
            ``@app.errorhandler(CsrfError)`` instead. This will be removed in
            version 1.0.

        The function will be passed one argument, ``reason``. By default it will
        raise a :class:`~flask_wtf.csrf.CsrfError`. ::

            @csrf.error_handler
            def csrf_error(reason):
                return render_template('error.html', reason=reason)

        Due to historical reasons, the function may either return a response
        or raise an exception with :func:`flask.abort`.
        """

        warnings.warn(FlaskWTFDeprecationWarning(
            '"@csrf.error_handler" is deprecated. Use the standard Flask error '
            'system with "@app.errorhandler(CsrfError)" instead. This will be'
            'removed in 1.0.'
        ), stacklevel=2)

        @wraps(view)
        def handler(reason):
            response = current_app.make_response(view(reason))
            raise CsrfError(response.get_data(as_text=True), response=response)

        self._error_response = handler
        return view


class CsrfError(BadRequest):
    """Raise if the client sends invalid CSRF data with the request.

    Generates a 400 Bad Request response with the failure reason by default.
    Customize the response by registering a handler with
    :meth:`flask.Flask.errorhandler`.
    """

    description = 'CSRF token missing or incorrect.'


def same_origin(current_uri, compare_uri):
    current = urlparse(current_uri)
    compare = urlparse(compare_uri)

    return (
        current.scheme == compare.scheme
        and current.hostname == compare.hostname
        and current.port == compare.port
    )
