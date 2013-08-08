# coding: utf-8
"""
    flask_wtf.i18n
    ~~~~~~~~~~~~~~

    Internationalization support for Flask WTF.

    :copyright: (c) 2013 by Hsiaoming Yang.
"""

from flask import _request_ctx_stack
from wtforms.ext.i18n.utils import messages_path
from flask.ext.babel import get_locale
from speaklater import make_lazy_string
from babel import support

__all__ = ('Translations', 'translations')


def _get_translations():
    """Returns the correct gettext translations.
    Copy from flask-babel with some modifications.
    """
    ctx = _request_ctx_stack.top
    if ctx is None:
        return None
    # babel should be in extensions for get_locale
    if 'babel' not in ctx.app.extensions:
        return None
    translations = getattr(ctx, 'wtforms_translations', None)
    if translations is None:
        dirname = messages_path()
        translations = support.Translations.load(
            dirname, [get_locale()], domain='wtforms'
        )
        ctx.wtforms_translations = translations
    return translations


def _gettext(string):
    t = _get_translations()
    if t is None:
        return string
    if hasattr(t, 'ugettext'):
        return t.ugettext(string)
    # Python 3 has no ugettext
    return t.gettext(string)


def _ngettext(singular, plural, n):
    t = _get_translations()
    if t is None:
        if n == 1:
            return singular
        return plural

    if hasattr(t, 'ungettext'):
        return t.ungettext(singular, plural, n)
    # Python 3 has no ungettext
    return t.ngettext(singular, plural, n)


class Translations(object):
    def gettext(self, string):
        return make_lazy_string(_gettext, string)

    def ngettext(self, singular, plural, n):
        return make_lazy_string(_ngettext, singular, plural, n)


translations = Translations()
