from wtforms.fields import Field

from flask.ext.wtf.recaptcha import widgets
from flask.ext.wtf.recaptcha.validators import Recaptcha

__all__ = ["RecaptchaField"]


class RecaptchaField(Field):
    widget = widgets.RecaptchaWidget()

    # error message if recaptcha validation fails
    recaptcha_error = None

    def __init__(self, label='', validators=None, **kwargs):
        validators = validators or [Recaptcha()]
        super(RecaptchaField, self).__init__(label, validators, **kwargs)
