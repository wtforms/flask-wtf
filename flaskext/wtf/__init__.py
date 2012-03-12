# -*- coding: utf-8 -*-
"""
    flaskext.wtf
    ~~~~~~~~~~~~

    Flask-WTF extension

    :copyright: (c) 2010 by Dan Jacob.
    :license: BSD, see LICENSE for more details.
"""

from wtforms.fields import BooleanField, DecimalField, DateField, \
    DateTimeField, FieldList, FloatField, FormField, \
    HiddenField, IntegerField, PasswordField, RadioField, SelectField, \
    SelectMultipleField, StringField, SubmitField, TextField, TextAreaField

from wtforms.validators import Email, email, EqualTo, equal_to, \
    IPAddress, ip_address, Length, length, MacAddress, mac_address, \
    NumberRange, number_range, Optional, optional, Required, required, Regexp, \
    regexp, UUID, URL, url, AnyOf, any_of, NoneOf, none_of

from wtforms.widgets import CheckboxInput, FileInput, HiddenInput, \
    ListWidget, Option, PasswordInput, RadioInput, Select, SubmitInput, \
    TableWidget, TextArea, TextInput

from wtforms.fields import FileField as _FileField

try:
    import sqlalchemy
    _is_sqlalchemy = True
except ImportError:
    _is_sqlalchemy = False


from wtforms import fields, widgets, validators, ValidationError

from flaskext.wtf import html5
from flaskext.wtf.form import Form
from flaskext.wtf import recaptcha

from flaskext.wtf.recaptcha.fields import RecaptchaField
from flaskext.wtf.recaptcha.widgets import RecaptchaWidget
from flaskext.wtf.recaptcha.validators import Recaptcha

fields.RecaptchaField = RecaptchaField
widgets.RecaptchaWidget = RecaptchaWidget
validators.Recaptcha = Recaptcha

from flaskext.wtf.file import FileField
from flaskext.wtf.file import FileAllowed, FileRequired, file_allowed, \
        file_required

fields.FileField = FileField

validators.file_allowed = file_allowed
validators.file_required = file_required
validators.FileAllowed = FileAllowed
validators.FileRequired = FileRequired


__all__  = ['Form', 'ValidationError',
            'fields', 'validators', 'widgets', 'html5']

__all__ += fields.core.__all__
__all__ += validators.__all__
__all__ += widgets.core.__all__
__all__ += recaptcha.__all__

if _is_sqlalchemy:
    from wtforms.ext.sqlalchemy.fields import QuerySelectField, \
        QuerySelectMultipleField

    __all__ += ['QuerySelectField', 
                'QuerySelectMultipleField']

    for field in (QuerySelectField, 
                  QuerySelectMultipleField):

        setattr(fields, field.__name__, field)

