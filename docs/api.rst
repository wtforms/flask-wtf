Developer Interface
===================

This part of the documentation covers all interfaces of Flask-WTF.

Forms and Fields
----------------

.. module:: flask_wtf

.. autoclass:: FlaskForm
    :members:

.. autoclass:: Form(...)

.. autoclass:: RecaptchaField

.. autoclass:: Recaptcha

.. autoclass:: RecaptchaWidget

.. module:: flask_wtf.file

.. autoclass:: FileField
   :members:

.. autoclass:: FileAllowed

.. autoclass:: FileRequired

CSRF Protection
---------------

.. module:: flask_wtf.csrf

.. autoclass:: CsrfProtect
   :members:

.. autofunction:: generate_csrf

.. autofunction:: validate_csrf
