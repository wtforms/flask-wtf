# coding: utf-8

import werkzeug.datastructures

from functools import wraps
from jinja2 import Markup, escape
from flask import (request, session, current_app, redirect, render_template,
                    url_for)
from wtforms.fields import HiddenField
from wtforms.widgets import HiddenInput
from wtforms.validators import ValidationError
from wtforms.ext.csrf.form import SecureForm
from ._compat import text_type, string_types
from .csrf import generate_csrf, validate_csrf

try:
    from .i18n import translations
except ImportError:
    translations = None  # babel not installed


class _Auto():
    '''Placeholder for unspecified variables that should be set to defaults.

    Used when None is a valid option and should not be replaced by a default.
    '''
    pass


def _is_hidden(field):
    """Detect if the field is hidden."""
    if isinstance(field, HiddenField):
        return True
    if isinstance(field.widget, HiddenInput):
        return True
    return False


class Form(SecureForm):
    """
    Flask-specific subclass of WTForms **SecureForm** class.

    If formdata is not specified, this will use flask.request.form.
    Explicitly pass formdata = None to prevent this.

    :param csrf_context: a session or dict-like object to use when making
                         CSRF tokens. Default: flask.session.

    :param secret_key: a secret key for building CSRF tokens. If this isn't
                       specified, the form will take the first of these
                       that is defined:

                       * SECRET_KEY attribute on this class
                       * WTF_CSRF_SECRET_KEY config of flask app
                       * SECRET_KEY config of flask app
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
        super(Form, self).__init__(
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
        """
        Checks if form has been submitted. The default case is if the HTTP
        method is **PUT** or **POST**.
        """

        return request and request.method in ("PUT", "POST")

    def hidden_tag(self, *fields):
        """
        Wraps hidden fields in a hidden DIV tag, in order to keep XHTML
        compliance.

        .. versionadded:: 0.3

        :param fields: list of hidden field names. If not provided will render
                       all hidden fields, including the CSRF field.
        """

        if not fields:
            fields = [f for f in self if _is_hidden(f)]

        name = current_app.config.get('WTF_HIDDEN_TAG', 'div')
        attrs = current_app.config.get(
            'WTF_HIDDEN_TAG_ATTRS', {'style': 'display:none;'})

        tag_attrs = u' '.join(
            u'%s="%s"' % (escape(k), escape(v)) for k, v in attrs.items())
        tag_start = u'<%s %s>' % (escape(name), tag_attrs)
        tag_end = u'</%s>' % escape(name)

        rv = [tag_start]
        for field in fields:
            if isinstance(field, string_types):
                field = getattr(self, field)
            rv.append(text_type(field))
        rv.append(tag_end)

        return Markup(u"".join(rv))

    def validate_on_submit(self):
        """
        Checks if form has been submitted and if so runs validate. This is
        a shortcut, equivalent to ``form.is_submitted() and form.validate()``
        """
        return self.is_submitted() and self.validate()

    @property
    def data(self):
        d = super(Form, self).data
        # https://github.com/lepture/flask-wtf/issues/208
        if self.csrf_enabled:
            d.pop('csrf_token', None)
        return d

    def _get_translations(self):
        if not current_app.config.get('WTF_I18N_ENABLED', True):
            return None
        return translations


def form_page(template, login_route, **parameters_to_render_template):
    """
    If you decorate a view with this, this will ensure that your HTML form
    has no fields blank, and allows the developer don't worry with the type
    of request is "POST" or "GET". For example::

        @app.route('/register', methods=["GET", "POST"])
        @form_page("register.html", ".register", title="Register user")
        def register():
            pass

    This feature is useful when you prefer using HTML to forms. It also allows
    less polluting your view, since it does not need to check which type
    of request or make validation of fields sent by HTML forms.

    :param template: Indicates the template page which contains the form.
        It is used if the request is of type "GET".
    :type template: string
    :param login_route: Indicates the route belonging to the form page.
        It is used if the HTML form is not valid.
    :type login_route: string
    :param parameters_to_render_template: Indicates the parameters to be
        passed to the template at the time of the request type "GET".
        For example, if we need to spend a title for our template, we use
        these parameters. Defaults to "None".
    :type parameters_to_render_template: any type.
    """
    def decorated_function(func):
        """
        :param func: The view function to decorate.
        :type func: function
        """
        @wraps(func)
        def decorated_view(*args, **kwargs):
            if request.method in ("POST", "PUT"):
                fields = request.form.to_dict()
                if _valid_form(fields):
                    return redirect(url_for(login_route))
                return func(*args, **kwargs)
            return render_template(template, **parameters_to_render_template)
        return decorated_view
    return decorated_function


def _valid_form(fields):
    """
    Check if form have empty fields.

    :param fields: Indicates a past dictionary with the parameters of the
        request "POST".
    :type fields: dict
    """
    fields_errors = {}
    for field in fields:
        field_value = fields[field]
        if field_value.isspace() or not len(field_value):
            fields_errors[field] = field_value
    return bool(fields_errors)
