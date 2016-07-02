# coding: utf-8
import warnings

import werkzeug.datastructures
from flask import request, session, current_app
from jinja2 import Markup
from wtforms.compat import with_metaclass
from wtforms.ext.csrf.form import SecureForm
from wtforms.form import FormMeta
from wtforms.validators import ValidationError
from wtforms.widgets import HiddenInput, SubmitInput

from ._compat import text_type, string_types, FlaskWTFDeprecationWarning
from .csrf import generate_csrf, validate_csrf

try:
    from .i18n import translations
except ImportError:
    translations = None  # babel not installed

SUBMIT_METHODS = set(('POST', 'PUT', 'PATCH', 'DELETE'))


class _Auto(object):
    """Placeholder for unspecified variables that should be set to defaults.

    Used when None is a valid option and should not be replaced by a default.
    """
    pass


class FlaskForm(SecureForm):
    """Flask-specific subclass of WTForms :class:`~wtforms.ext.csrf.form.SecureForm` class.

    If ``formdata`` is not specified, this will use :attr:`flask.request.form` and
    :attr:`flask.request.files`.  Explicitly pass ``formdata=None`` to prevent this.

    :param csrf_context: a session or dict-like object to use when making
        CSRF tokens. Default: :data:`flask.session`.

    :param secret_key: a secret key for building CSRF tokens. If this isn't
        specified, the form will take the first of these
        that is defined:

        * SECRET_KEY attribute on this class
        * WTF_CSRF_SECRET_KEY config of Flask app
        * SECRET_KEY config of Flask app
        * session secret key

    :param csrf_enabled: whether to use CSRF protection. If False, all
        csrf behavior is suppressed.
        Default: WTF_CSRF_ENABLED config value
    """

    SECRET_KEY = None
    TIME_LIMIT = None

    def __init__(self, formdata=_Auto, obj=None, prefix='', csrf_context=None,
                 secret_key=None, csrf_enabled=None, **kwargs):

        if csrf_enabled is None:
            csrf_enabled = current_app.config.get('WTF_CSRF_ENABLED', True)

        self.csrf_enabled = csrf_enabled

        if formdata is _Auto:
            if self.is_submitted():
                formdata = request.form
                if request.files:
                    formdata = formdata.copy()
                    formdata.update(request.files)
                elif request.get_json():
                    formdata = werkzeug.datastructures.MultiDict(request.get_json())
            else:
                formdata = None

        if self.csrf_enabled:
            if csrf_context is None:
                csrf_context = session
            if secret_key is None:
                # It wasn't passed in, check if the class has a SECRET_KEY
                secret_key = getattr(self, "SECRET_KEY", None)

            self.SECRET_KEY = secret_key
        else:
            csrf_context = {}
            self.SECRET_KEY = ''
        super(FlaskForm, self).__init__(
            formdata, obj, prefix,
            csrf_context=csrf_context,
            **kwargs
        )

    def generate_csrf_token(self, csrf_context=None):
        if not self.csrf_enabled:
            return None
        return generate_csrf(self.SECRET_KEY, self.TIME_LIMIT)

    def validate_csrf_token(self, field):
        if not self.csrf_enabled:
            return True
        if hasattr(request, 'csrf_valid') and request.csrf_valid:
            # this is validated by CsrfProtect
            return True
        if not validate_csrf(field.data, self.SECRET_KEY, self.TIME_LIMIT):
            raise ValidationError(field.gettext('CSRF token missing'))

    def validate_csrf_data(self, data):
        """Check if the csrf data is valid.

        .. versionadded: 0.9.0

        :param data: the csrf string to be validated.
        """
        return validate_csrf(data, self.SECRET_KEY, self.TIME_LIMIT)

    def is_submitted(self):
        """Consider the form submitted if there is an active request and
        the method is ``POST``, ``PUT``, ``PATCH``, or ``DELETE``.
        """

        return request and request.method in SUBMIT_METHODS

    def hidden_tag(self, *fields):
        """Render the form's hidden fields in one call.

        A field is considered hidden if it uses the
        :class:`~wtforms.widgets.HiddenInput` widget.

        If ``fields`` are given, only render the given fields that
        are hidden.  If a string is passed, render the field with that
        name if it exists.

        .. versionchanged:: 0.13

           No longer wraps inputs in hidden div.
           This is valid HTML 5.

        .. versionchanged:: 0.13

           Skip passed fields that aren't hidden.
           Skip passed names that don't exist.
        """

        def hidden_fields(fields):
            for f in fields:
                if isinstance(f, string_types):
                    f = getattr(self, f, None)

                if f is None or not isinstance(f.widget, HiddenInput):
                    continue

                yield f

        return Markup(u'\n'.join(text_type(f) for f in hidden_fields(fields or self)))

    def validate_on_submit(self):
        """Call :meth:`validate` only if the form is submitted.
        This is a shortcut for ``form.is_submitted() and form.validate()``.
        """
        return self.is_submitted() and self.validate()

    @property
    def data(self):
        d = super(FlaskForm, self).data
        # https://github.com/lepture/flask-wtf/issues/208
        if self.csrf_enabled:
            d.pop('csrf_token', None)
        return d

    def _get_translations(self):
        if not current_app.config.get('WTF_I18N_ENABLED', True):
            return None
        return translations


class DeprecatedFormMeta(FormMeta):
    def __init__(cls, name, bases, attrs):
        warnings.warn(FlaskWTFDeprecationWarning(
            '"flask_wtf.Form" has been renamed to "FlaskForm" '
            'and will be removed in 1.0.'
        ), stacklevel=2)
        type.__init__(cls, name, bases, attrs)


class Form(with_metaclass(DeprecatedFormMeta, FlaskForm)):
    """
    .. deprecated:: 0.13
        Renamed to :class:`~flask_wtf.FlaskForm`.
    """
