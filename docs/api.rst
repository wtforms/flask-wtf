Developer Interface
===================

This part of the documentation covers all interfaces of Flask-WTF.

Forms and Fields
----------------

.. module:: flask_wtf

.. autoclass:: Form
   :members:

.. autoclass:: RecaptchaField

.. autoclass:: Recaptcha

.. autoclass:: RecaptchaWidget

.. module:: flask_wtf.file

.. autoclass:: FileField
   :members:

.. autoclass:: FileAllowed

.. autoclass:: FileRequired

.. module:: flask_wtf.html5

.. autoclass:: SearchInput

.. autoclass:: SearchField

.. autoclass:: URLInput

.. autoclass:: URLField

.. autoclass:: EmailInput

.. autoclass:: EmailField

.. autoclass:: TelInput

.. autoclass:: TelField

.. autoclass:: NumberInput

.. autoclass:: IntegerField

.. autoclass:: DecimalField

.. autoclass:: RangeInput

.. autoclass:: IntegerRangeField

.. autoclass:: DecimalRangeField


CSRF Protection
---------------

.. module:: flask_wtf.csrf

.. autoclass:: CsrfProtect
   :members:

.. autofunction:: generate_csrf

.. autofunction:: validate_csrf
