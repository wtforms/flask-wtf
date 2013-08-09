Creating Forms
==============

This part of the documentation covers the Form parts.

Secure Form
-----------

.. module:: flask_wtf

Without any configuration, the :class:`Form` will be a session secure
form with csrf protection. We encourage you do nothing.

But if you want to disable the csrf protection, you can pass::

    form = Form(csrf_enabled=False)

If you want to disable it globally, which you really shouldn't. But if
you insist, it can be done with the configuration::

    WTF_CSRF_ENABLED = False

In order to generate the csrf token, you need to has a secret key, this
is usually the same as your Flask app secret key. If you want to use
another secret key, config it::

    WTF_CSRF_SECRET_KEY = 'a random string'


File Uploads
------------

HTML5 Widgets
-------------

Recaptcha
---------
