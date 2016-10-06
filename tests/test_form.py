import warnings
from unittest import TestCase
from flask_wtf import Form
from flask_wtf._compat import FlaskWTFDeprecationWarning
from wtforms.compat import with_metaclass
from wtforms.form import FormMeta


class TestForm(TestCase):
    def test_deprecated_form(self):
        with warnings.catch_warnings():
            warnings.simplefilter('error', FlaskWTFDeprecationWarning)

            class F1(Form):
                pass

            self.assertRaises(FlaskWTFDeprecationWarning, F1)

            class FMeta(FormMeta):
                pass

            class F2(with_metaclass(FMeta, Form)):
                pass

            self.assertRaises(FlaskWTFDeprecationWarning, F2)

    def test_deprecated_html5(self):
        with warnings.catch_warnings():
            warnings.simplefilter('error', FlaskWTFDeprecationWarning)
            self.assertRaises(FlaskWTFDeprecationWarning, __import__, 'flask_wtf.html5')
