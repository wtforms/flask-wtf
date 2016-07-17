# coding: utf-8
"""
    flask_wtf.i18n
    ~~~~~~~~~~~~~~

    Internationalization support for Flask WTF.

    :copyright: (c) 2013 by Hsiaoming Yang.
"""

import os

from flask import _request_ctx_stack

try:
    from babel import support
    from speaklater import make_lazy_string
except ImportError:
    # Babel or speaklater is not found, so
    # we expect `make_lazy_string` to return just the value:
    support = None
    make_lazy_string = lambda x, *args, **kwargs: x

try:
    from flask_babel import get_locale
except ImportError:
    from flask_babelex import get_locale

try:
    from wtforms.i18n import messages_path as wtf_messages
except ImportError:
    from wtforms.ext.i18n.utils import messages_path as wtf_messages


__all__ = ('Translations', 'translations')


def _messages_path():
    """
    Determine the path to the 'messages' directory as best possible.

    This is the exact copy of `wtforms`'s `messages_path`,
    except for the paths itself. This version points to the `./locale`
    """
    module_path = os.path.abspath(__file__)
    locale_path = os.path.join(os.path.dirname(module_path), 'locale')
    if not os.path.exists(locale_path):
        locale_path = '/usr/share/locale'
    return locale_path


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

    _translations = getattr(ctx, 'wtforms_translations', None)
    if _translations is None and support:
        _translations = support.Translations.load(
            wtf_messages(), [get_locale()], domain='wtforms'
        )

        wtf_forms_translations = support.Translations.load(
            _messages_path(), [get_locale()], domain='flask_wtf'
        )
        ctx.wtforms_translations = _translations.merge(
            # Basic `wtforms` translations with the same messages
            # will be overridden by our messages:
            wtf_forms_translations
        )
    return _translations


class Translations(object):
    def gettext(self, string):
        t = _get_translations()
        if t is None:
            return string
        if hasattr(t, 'ugettext'):
            return t.ugettext(string)
        # Python 3 has no ugettext
        return t.gettext(string)

    def ngettext(self, singular, plural, n):
        t = _get_translations()
        if t is None:
            if n == 1:
                return singular
            return plural

        if hasattr(t, 'ungettext'):
            return t.ungettext(singular, plural, n)
        # Python 3 has no ungettext
        return t.ngettext(singular, plural, n)

    def lazy_gettext(self, string, **variables):
        """
        This string will be evaluated at the actual response.
        """
        return make_lazy_string(self.gettext, string, **variables)


translations = Translations()
