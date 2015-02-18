Configuration
=============

Here is the full table of all configurations.

Forms and CSRF
--------------

The full list of configuration for Flask-WTF. Usually, you don't need
to configure any of them. It just works.

======================= ==============================================
WTF_CSRF_ENABLED        Disable/enable CSRF protection for forms.
                        Default is True.
WTF_CSRF_CHECK_DEFAULT  Enable CSRF checks for all views by default.
                        Default is True.
WTF_I18N_ENABLED        Disable/enable I18N support. This should work
                        together with Flask-Babel. Default is True.
WTF_CSRF_HEADERS        CSRF token HTTP headers checked. Default is
                        **['X-CSRFToken', 'X-CSRF-Token']**
WTF_CSRF_SECRET_KEY     A random string for generating CSRF token.
                        Default is the same as SECRET_KEY.
WTF_CSRF_TIME_LIMIT     CSRF token expiring time. Default is **3600**
                        seconds.
WTF_CSRF_SSL_STRICT     Strictly protection on SSL. This will check
                        the referrer, validate if it is from the same
                        origin. Default is True.
WTF_CSRF_METHODS        CSRF protection on these request methods.
                        Default is **['POST', 'PUT', 'PATCH']**
WTF_HIDDEN_TAG          HTML tag name of the hidden tag wrapper.
                        Default is **div**
WTF_HIDDEN_TAG_ATTRS    HTML tag attributes of the hidden tag wrapper.
                        Default is **{'style': 'display:none;'}**
======================= ==============================================


Recaptcha
---------

You have already learned these configuration at :ref:`recaptcha`.
This table is only designed for a convience.

======================= ==============================================
RECAPTCHA_USE_SSL       Enable/disable recaptcha through ssl.
                        Default is False.
RECAPTCHA_PUBLIC_KEY    **required** A public key.
RECAPTCHA_PRIVATE_KEY   **required** A private key.
RECAPTCHA_OPTIONS       **optional** A dict of configuration options.
                        https://www.google.com/recaptcha/admin/create
======================= ==============================================
