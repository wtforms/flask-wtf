import widgets
import validators

from wtforms.fields import Field

__all__ = ["RecaptchaField"]

class RecaptchaField(Field):
    widget = widgets.RecaptchaWidget()
    validators = [validators.Recaptcha()]

    # error message if recaptcha validation fails
    recaptcha_error = None

