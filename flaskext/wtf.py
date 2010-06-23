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
    DateTimeField, FieldList, FileField, FloatField, FormField,\
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
    # try to import sqlalchemy-based fields
    # otherwise ignore
    from wtforms.ext.sqlalchemy.fields import QuerySelectField, \
        QuerySelectMultipleField, ModelSelectField
    _is_sqlalchemy = True
except ImportError:
    _is_sqlalchemy = False


from wtforms import Form as BaseForm
from wtforms import fields, widgets, validators, ValidationError

from flask import request, session, current_app

from jinja2 import Markup

__all__  = ['Form', 'ValidationForm', 'fields', 'validators', 'widgets']
__all__ += fields.__all__
__all__ += validators.__all__
__all__ += widgets.__all__

if _is_sqlalchemy:
    __all__ += ['QuerySelectField', 
                'QuerySelectMultipleField',
                'ModelSelectField']

def _generate_csrf_token():
    return str(uuid.uuid4())

class Form(BaseForm):

    csrf = fields.HiddenField()

    def __init__(self, formdata=None, *args, **kwargs):

        if formdata is None:
            formdata = request.form

        self.csrf_enabled = kwargs.pop('csrf_enabled', True)
        self.csrf_enabled = self.csrf_enabled and \
            current_app.config.get('CSRF_ENABLED', True)
        
        csrf_token = session.get('_csrf_token', None)
        if csrf_token is None:
            csrf_token = self.reset_csrf()

        super(Form, self).__init__(formdata, csrf=csrf_token, *args, **kwargs)
    
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
        session['_csrf_token'] = csrf_token
        return csrf_token

    def validate_csrf(self, field):
        if not self.csrf_enabled or request.is_xhr:
            return
        csrf_token = session.pop('_csrf_token', None)
        if not field.data or field.data != csrf_token:
            raise ValidationError, "Missing or invalid CSRF token"

    def validate_on_submit(self):
        return request.method in ("POST", "PUT") and self.validate()
    

