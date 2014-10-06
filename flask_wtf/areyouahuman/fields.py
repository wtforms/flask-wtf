from wtforms.fields import Field

from . import widgets
from .validators import AreYouAHuman

__all__ = ["AreYouAHumanField"]


class AreYouAHumanField(Field):
    widget = widgets.AreYouAHumanWidget()

    # error message if AreYouAHuman validation fails
    areyouahuman_error = None

    def __init__(self, label='', validators=None, **kwargs):
        validators = validators or [AreYouAHuman()]
        super(AreYouAHumanField, self).__init__(label, validators, **kwargs)
