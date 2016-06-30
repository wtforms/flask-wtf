import warnings
from unittest import TestCase
from flask_wtf import Form
from flask_wtf._compat import FlaskWTFDeprecationWarning


class TestForm(TestCase):
    def test_deprecated_form(self):
        def define_deprecated_form():
            class F(Form):
                pass

        with warnings.catch_warnings():
            warnings.simplefilter('error', FlaskWTFDeprecationWarning)
            self.assertRaises(FlaskWTFDeprecationWarning, define_deprecated_form)
