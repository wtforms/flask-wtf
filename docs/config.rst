Configuration
=============

========================== =====================================================
``WTF_CSRF_ENABLED``       Set to ``False`` to disable all CSRF protection. 
                           Default is ``True``.
``WTF_CSRF_CHECK_DEFAULT`` When using the CSRF protection extension, this
                           controls whether every view is protected by default.
                           Default is ``True``.
``WTF_CSRF_SECRET_KEY``    Random data for generating secure tokens. If this is
                           not set then ``SECRET_KEY`` is used.
``WTF_CSRF_METHODS``       HTTP methods to protect from CSRF. Default is
                           ``{'POST', 'PUT', 'PATCH', 'DELETE'}``.
``WTF_CSRF_FIELD_NAME``    Name of the form field and session key that holds the
                           CSRF token. Default is ``csrf_token``.
``WTF_CSRF_HEADERS``       HTTP headers to search for CSRF token when it is not
                           provided in the form. Default is
                           ``['X-CSRFToken', 'X-CSRF-Token']``.
``WTF_CSRF_TIME_LIMIT``    Max age in seconds for CSRF tokens. Default is
                           ``3600``. If set to ``None``, the CSRF token is valid
                           for the life of the session.
``WTF_CSRF_SSL_STRICT``    Whether to enforce the same origin policy by checking
                           that the referrer matches the host. Only applies to
                           HTTPS requests. Default is ``True``.
``WTF_I18N_ENABLED``       Set to ``False`` to disable Flask-Babel I18N support.
                           Also set to ``False`` if you want to use WTForms's 
                           built-in messages directly, see more info `here`_.
                           Default is ``True``.
========================== =====================================================

.. _here: https://wtforms.readthedocs.io/en/stable/i18n.html#using-the-built-in-translations-provider

Recaptcha
---------

========================= ==============================================
``RECAPTCHA_PUBLIC_KEY``  **required** A public key.
``RECAPTCHA_PRIVATE_KEY`` **required** A private key.
                          https://www.google.com/recaptcha/admin
``RECAPTCHA_PARAMETERS``  **optional** A dict of configuration options.
``RECAPTCHA_HTML``        **optional** Override default HTML template
                          for Recaptcha.
``RECAPTCHA_DATA_ATTRS``  **optional** A dict of ``data-`` attrs to use
                          for Recaptcha div
========================= ==============================================

Logging
-------

CSRF errors are logged at the ``INFO`` level to the ``flask_wtf.csrf`` logger.
You still need to configure logging in your application in order to see these
messages.
