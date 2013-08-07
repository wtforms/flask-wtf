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
from datetime import datetime, timedelta
from flask import current_app, session, request, abort
from ._compat import to_bytes


TIME_FORMAT = '%Y%m%d%H%M%S'


def generate_csrf(secret_key=None, time_limit=30):
    """Generate csrf token code.

    :param secret_key: A secret key for mixing in the token,
                       default is Flask.secret_key.
    :param time_limit: Token valid in the time limit,
                       default is 30 minutes.
    """
    if not secret_key:
        secret_key = current_app.secret_key

    if 'csrf_token' not in session:
        session['csrf_token'] = hashlib.sha1(os.urandom(64)).hexdigest()

    if time_limit:
        if not isinstance(time_limit, timedelta):
            time_limit = timedelta(minutes=time_limit)
        expires = (datetime.now() + time_limit).strftime(TIME_FORMAT)
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

    if time_limit:
        now = datetime.now().strftime(TIME_FORMAT)
        if now > expires:
            # refresh session
            session.pop('csrf_token', None)
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


def csrf_protect(app, on_csrf=None):
    """Enable csrf protect for Flask."""

    app.config['WTF_CSRF_PROTECT'] = True
    secret_key = app.config.get('WTF_CSRF_SECRET_KEY', app.secret_key)

    @app.before_request
    def _csrf_protect():
        if app.testing:
            return
        if not request.method == 'POST':
            return

        csrf_token = request.form.get('csrf_token')
        if not validate_csrf(csrf_token, secret_key):
            if on_csrf:
                on_csrf(*app.match_request())
            return abort(400)

    app.jinja_env.globals['csrf_token'] = generate_csrf
