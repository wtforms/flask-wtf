# -*- coding: utf-8 -*-

from wtforms.fields import Field

from . import widgets
from .validators import YandexCaptcha

__all__ = ['YandexCaptchaField']


class YandexCaptchaField(Field):
    widget = widgets.YandexCaptchaWidget()

    recaptcha_error = None

    def __init__(self, label='', validators=None, **kwargs):
        validators = validators or [YandexCaptcha()]
        super(YandexCaptchaField, self).__init__(label, validators, **kwargs)