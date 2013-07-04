# coding: utf-8
# flake8: noqa
from wtforms.widgets.html5 import *
from wtforms.fields.html5 import *

from wtforms.widgets.core import Input

# wtforms missing DateInput

class DateInput(Input):
    input_type = 'date'
