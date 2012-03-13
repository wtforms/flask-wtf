# -*- coding: utf-8 -*-
"""
    flaskext.wtf
    ~~~~~~~~~~~~

    Flask-WTF extension

    :copyright: (c) 2010 by Dan Jacob.
    :license: BSD, see LICENSE for more details.
"""

try:
    import sqlalchemy
    _is_sqlalchemy = True
except ImportError:
    _is_sqlalchemy = False

from wtforms import fields, widgets, validators
from wtforms.fields import *
from wtforms.validators import *
from wtforms.widgets import *
from wtforms import ValidationError

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

__all__ += validators.__all__
__all__ += fields.__all__ if hasattr(fields, '__all__') else fields.core.__all__
__all__ += widgets.__all__ if hasattr(widgets, '__all__') else widgets.core.__all__
__all__ += recaptcha.__all__

if _is_sqlalchemy:
    from wtforms.ext.sqlalchemy.fields import QuerySelectField, \
        QuerySelectMultipleField

    __all__ += ['QuerySelectField', 
                'QuerySelectMultipleField']

    for field in (QuerySelectField, 
                  QuerySelectMultipleField):

        setattr(fields, field.__name__, field)

