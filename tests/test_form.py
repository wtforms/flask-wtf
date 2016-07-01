import warnings
from unittest import TestCase
from flask_wtf import Form
from flask_wtf._compat import FlaskWTFDeprecationWarning


class TestForm(TestCase):
    def test_deprecated_form(self):
        with warnings.catch_warnings():
            warnings.simplefilter('error', FlaskWTFDeprecationWarning)
            self.assertRaises(FlaskWTFDeprecationWarning, type, 'F', (Form,), {})

    def test_deprecated_html5(self):
        with warnings.catch_warnings():
            warnings.simplefilter('error', FlaskWTFDeprecationWarning)
            self.assertRaises(FlaskWTFDeprecationWarning, __import__, 'flask_wtf.html5')
