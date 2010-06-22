# -*- coding: utf-8 -*-
"""
    flaskext.wtf
    ~~~~~~~~~~~~

    Description of the module goes here...

    :copyright: (c) 2010 by Dan Jacob.
    :license: BSD, see LICENSE for more details.
"""
import uuid

from wtforms.fields import *
from wtforms.validators import *

from wtforms import Form as BaseForm
from wtforms import fields, validators, ValidationError

from flask import request, session, current_app

__all__  = ['Form', 'ValidationForm', 'fields', 'validators']
__all__ += fields.__all__
__all__ += validators.__all__

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
        
        csrf_token = session.get('_csrf_token')
        if csrf_token is None:
            csrf_token = _generate_csrf_token()
            session['_csrf_token'] = csrf_token

        super(Form, self).__init__(formdata, csrf=csrf_token, *args, **kwargs)

    def validate_csrf(self, field):
        if not self.csrf_enabled or request.is_xhr:
            return
        csrf_token = session.pop('_csrf_token', None)
        if not field.data or field.data != csrf_token:
            raise ValidationError, "Missing or invalid CSRF token"

    def validate_on_POST(self):
        return request.method == "POST" and self.validate()

