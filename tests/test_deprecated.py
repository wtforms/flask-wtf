import warnings
from unittest import TestCase

from wtforms.compat import with_metaclass
from wtforms.form import FormMeta

from flask_wtf import CsrfProtect, FlaskForm, Form
from flask_wtf._compat import FlaskWTFDeprecationWarning


class TestDeprecated(TestCase):
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

    def test_deprecated_csrf_enabled(self):
        class F(FlaskForm):
            pass

        with warnings.catch_warnings():
            warnings.simplefilter('error', FlaskWTFDeprecationWarning)
            self.assertRaises(FlaskWTFDeprecationWarning, F, csrf_enabled=False)

    def test_deprecated_csrfprotect(self):
        with warnings.catch_warnings():
            warnings.simplefilter('error', FlaskWTFDeprecationWarning)
            self.assertRaises(FlaskWTFDeprecationWarning, CsrfProtect)
