# -*- coding: utf-8 -*-
"""
    flaskext.wtf
    ~~~~~~~~~~~~

    Description of the module goes here...

    :copyright: (c) 2010 by Dan Jacob.
    :license: BSD, see LICENSE for more details.
"""

import uuid

from wtforms.fields import BooleanField, DecimalField, DateField, \
    DateTimeField, FieldList, FloatField, FileField, FormField, \
    HiddenField, IntegerField, PasswordField, RadioField, SelectField, \
    SelectMultipleField, SubmitField, TextField, TextAreaField

from wtforms.validators import Email, email, EqualTo, equal_to, \
    IPAddress, ip_address, Length, length, NumberRange, number_range, \
    Optional, optional, Required, required, Regexp, regexp, \
    URL, url, AnyOf, any_of, NoneOf, none_of

from wtforms.widgets import CheckboxInput, FileInput, HiddenInput, \
    ListWidget, PasswordInput, RadioInput, Select, SubmitInput, \
    TableWidget, TextArea, TextInput

try:
    import sqlalchemy
    _is_sqlalchemy = True
except ImportError:
    _is_sqlalchemy = False


from wtforms import Form as BaseForm
from wtforms import fields, widgets, validators, ValidationError

from flask import request, session, current_app

from jinja2 import Markup

from flaskext.wtf import recaptcha

from flaskext.wtf.recaptcha.fields import RecaptchaField
from flaskext.wtf.recaptcha.widgets import RecaptchaWidget
from flaskext.wtf.recaptcha.validators import Recaptcha

fields.RecaptchaField = RecaptchaField
fields.RecaptchaWidget = RecaptchaWidget
fields.Recaptcha = Recaptcha

__all__  = ['Form', 'ValidationForm',
            'fields', 'validators', 'widgets']

__all__ += fields.__all__
__all__ += validators.__all__
__all__ += widgets.__all__
__all__ += recaptcha.__all__

if _is_sqlalchemy:
    from wtforms.ext.sqlalchemy.fields import QuerySelectField, \
        QuerySelectMultipleField, ModelSelectField

    __all__ += ['QuerySelectField', 
                'QuerySelectMultipleField',
                'ModelSelectField']

    for field in (QuerySelectField, 
                  QuerySelectMultipleField,
                  ModelSelectField):

        setattr(fields, field.__name__, field)


def _generate_csrf_token():
    return str(uuid.uuid4())


class Form(BaseForm):

    csrf = fields.HiddenField()

    def __init__(self, formdata=None, *args, **kwargs):

        csrf_enabled = kwargs.pop('csrf_enabled', None)

        if csrf_enabled is None:
            csrf_enabled = current_app.config.get('CSRF_ENABLED', True)
        
        self.csrf_enabled = csrf_enabled

        self.csrf_session_key = kwargs.pop('csrf_session_key', None)

        if self.csrf_session_key is None:
            self.csrf_session_key = \
                current_app.config.get('CSRF_SESSION_KEY', '_csrf_token')

        csrf_token = session.get(self.csrf_session_key, None)

        if csrf_token is None:
            csrf_token = self.reset_csrf()

        super(Form, self).__init__(formdata, csrf=csrf_token, *args, **kwargs)

    def is_submitted(self):

        return request and request.method in ("PUT", "POST")

    def process(self, formdata=None, obj=None, **kwargs):

        if self.is_submitted():
        
            if formdata is None:
                formdata = request.form

            if request.files:

                for name, field in self._fields.iteritems():
                    if isinstance(field, FileField) and name in request.files:
                        field.file = request.files[name]

        super(Form, self).process(formdata, obj, **kwargs)

    @property
    def csrf_token(self):
        """
        Renders CSRF field inside a hidden DIV.
        """
        return Markup('<div style="display:none;">%s</div>' % self.csrf)

    def reset_csrf(self):
        """
        Resets the CSRF token in the session. If you are reusing the form
        in the same view (i.e. you are not redirecting somewhere else)
        it's recommended you call this before rendering the form.
        """
        
        csrf_token = _generate_csrf_token()
        session[self.csrf_session_key] = csrf_token
        return csrf_token

    def validate_csrf(self, field):
        if not self.csrf_enabled or request.is_xhr:
            return

        csrf_token = session.pop(self.csrf_session_key, None)
        is_valid = field.data and field.data == csrf_token

        # reset this field, otherwise stale token is displayed
        field.data = self.reset_csrf()

        if not is_valid:
            raise ValidationError, "Missing or invalid CSRF token"

    def validate_on_submit(self):
        return self.is_submitted() and self.validate()
    

