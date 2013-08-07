# -*- coding: utf-8 -*-
"""
    flask.ext.wtf
    ~~~~~~~~~~~~

    Flask-WTF extension

    :copyright: (c) 2010 by Dan Jacob.
    :license: BSD, see LICENSE for more details.
"""
# flake8: noqa
from __future__ import absolute_import

from wtforms import fields, widgets, validators
from wtforms.fields import *
from wtforms.validators import *
from wtforms.widgets import *

from .form import Form
from . import html5
from . import recaptcha

from .recaptcha.fields import RecaptchaField
from .recaptcha.widgets import RecaptchaWidget
from .recaptcha.validators import Recaptcha

fields.RecaptchaField = RecaptchaField
widgets.RecaptchaWidget = RecaptchaWidget
validators.Recaptcha = Recaptcha

from .file import FileField
from .file import FileAllowed, FileRequired
from .file import file_allowed, file_required

fields.FileField = FileField

validators.file_allowed = file_allowed
validators.file_required = file_required
validators.FileAllowed = FileAllowed
validators.FileRequired = FileRequired
