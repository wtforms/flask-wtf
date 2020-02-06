Flask-WTF Changelog
===================

Version 0.14.3
--------------

Released 2020-02-06

-   Fix deprecated imports from ``werkzeug`` and ``collections``.


Version 0.14.2
--------------

Released 2017-01-10

- Fix bug where ``FlaskForm`` assumed ``meta`` argument was not ``None`` if it
  was passed. (`#278`_)

.. _#278: https://github.com/lepture/flask-wtf/issues/278

Version 0.14.1
--------------

Released 2017-01-10

- Fix bug where the file validators would incorrectly identify an empty file as
  valid data. (`#276`_, `#277`_)

    - ``FileField`` is no longer deprecated. The data is checked during
      processing and only set if it's a valid file.
    - ``has_file`` *is* deprecated; it's now equivalent to ``bool(field.data)``.
    - ``FileRequired`` and ``FileAllowed`` work with both the Flask-WTF and
      WTForms ``FileField`` classes.
    - The ``Optional`` validator now works with ``FileField``.

.. _#276: https://github.com/lepture/flask-wtf/issues/276
.. _#277: https://github.com/lepture/flask-wtf/pull/277

Version 0.14
------------

Released 2017-01-06

- Use itsdangerous to sign CSRF tokens and check expiration instead of doing it
  ourselves. (`#264`_)

    - All tokens are URL safe, removing the ``url_safe`` parameter from
      ``generate_csrf``. (`#206`_)
    - All tokens store a timestamp, which is checked in ``validate_csrf``. The
      ``time_limit`` parameter of ``generate_csrf`` is removed.

- Remove the ``app`` attribute from ``CsrfProtect``, use ``current_app``.
  (`#264`_)
- ``CsrfProtect`` protects the ``DELETE`` method by default. (`#264`_)
- The same CSRF token is generated for the lifetime of a request. It is exposed
  as ``g.csrf_token`` for use during testing. (`#227`_, `#264`_)
- ``CsrfProtect.error_handler`` is deprecated. (`#264`_)

    - Handlers that return a response work in addition to those that raise an
      error. The behavior was not clear in previous docs.
    - (`#200`_, `#209`_, `#243`_, `#252`_)

- Use ``Form.Meta`` instead of deprecated ``SecureForm`` for CSRF (and
  everything else). (`#216`_, `#271`_)

    - ``csrf_enabled`` parameter is still recognized but deprecated. All other
      attributes and methods from ``SecureForm`` are removed. (`#271`_)

- Provide ``WTF_CSRF_FIELD_NAME`` to configure the name of the CSRF token.
  (`#271`_)
- ``validate_csrf`` raises ``wtforms.ValidationError`` with specific messages
  instead of returning ``True`` or ``False``. This breaks anything that was
  calling the method directly. (`#239`_, `#271`_)

    - CSRF errors are logged as well as raised. (`#239`_)

- ``CsrfProtect`` is renamed to ``CSRFProtect``. A deprecation warning is issued
  when using the old name. ``CsrfError`` is renamed to ``CSRFError`` without
  deprecation. (`#271`_)
- ``FileField`` is deprecated because it no longer provides functionality over
  the provided validators. Use ``wtforms.FileField`` directly. (`#272`_)

.. _`#200`: https://github.com/lepture/flask-wtf/issues/200
.. _`#209`: https://github.com/lepture/flask-wtf/pull/209
.. _`#216`: https://github.com/lepture/flask-wtf/issues/216
.. _`#227`: https://github.com/lepture/flask-wtf/issues/227
.. _`#239`: https://github.com/lepture/flask-wtf/issues/239
.. _`#243`: https://github.com/lepture/flask-wtf/pull/243
.. _`#252`: https://github.com/lepture/flask-wtf/pull/252
.. _`#264`: https://github.com/lepture/flask-wtf/pull/264
.. _`#271`: https://github.com/lepture/flask-wtf/pull/271
.. _`#272`: https://github.com/lepture/flask-wtf/pull/272

Version 0.13.1
--------------

Released 2016/10/6

- Deprecation warning for ``Form`` is shown during ``__init__`` instead of immediately when subclassing. (`#262`_)
- Don't use ``pkg_resources`` to get version, for compatibility with GAE. (`#261`_)

.. _`#261`: https://github.com/lepture/flask-wtf/issues/261
.. _`#262`: https://github.com/lepture/flask-wtf/issues/262

Version 0.13
------------

Released 2016/09/29

- ``Form`` is renamed to ``FlaskForm`` in order to avoid name collision with WTForms's base class.  Using ``Form`` will show a deprecation warning. (`#250`_)
- ``hidden_tag`` no longer wraps the hidden inputs in a hidden div.  This is valid HTML5 and any modern HTML parser will behave correctly. (`#217`_, `#193`_)
- ``flask_wtf.html5`` is deprecated.  Import directly from ``wtforms.fields.html5``. (`#251`_)
- ``is_submitted`` is true for ``PATCH`` and ``DELETE`` in addition to ``POST`` and ``PUT``. (`#187`_)
- ``generate_csrf`` takes a ``token_key`` parameter to specify the key stored in the session. (`#206`_)
- ``generate_csrf`` takes a ``url_safe`` parameter to allow the token to be used in URLs. (`#206`_)
- ``form.data`` can be accessed multiple times without raising an exception. (`#248`_)
- File extension with multiple parts (``.tar.gz``) can be used in the ``FileAllowed`` validator. (`#201`_)

.. _`#187`: https://github.com/lepture/flask-wtf/pull/187
.. _`#193`: https://github.com/lepture/flask-wtf/issues/193
.. _`#201`: https://github.com/lepture/flask-wtf/issues/201
.. _`#206`: https://github.com/lepture/flask-wtf/pull/206
.. _`#217`: https://github.com/lepture/flask-wtf/issues/217
.. _`#248`: https://github.com/lepture/flask-wtf/pull/248
.. _`#250`: https://github.com/lepture/flask-wtf/pull/250
.. _`#251`: https://github.com/lepture/flask-wtf/pull/251

Version 0.12
------------

Released 2015/07/09

- Abstract protect_csrf() into a separate method
- Update reCAPTCHA configuration
- Fix reCAPTCHA error handle

Version 0.11
------------

Released 2015/01/21

- Use the new reCAPTCHA API via `#164`_.

.. _`#164`: https://github.com/lepture/flask-wtf/pull/164


Version 0.10.3
--------------

Released 2014/11/16

- Add configuration: WTF_CSRF_HEADERS via `#159`_.
- Support customize hidden tags via `#150`_.
- And many more bug fixes

.. _`#150`: https://github.com/lepture/flask-wtf/pull/150
.. _`#159`: https://github.com/lepture/flask-wtf/pull/159

Version 0.10.2
--------------

Released 2014/09/03

- Update translation for reCaptcha via `#146`_.

.. _`#146`: https://github.com/lepture/flask-wtf/pull/146


Version 0.10.1
--------------

Released 2014/08/26

- Update RECAPTCHA API SERVER URL via `#145`_.
- Update requirement Werkzeug>=0.9.5
- Fix CsrfProtect exempt for blueprints via `#143`_.

.. _`#145`: https://github.com/lepture/flask-wtf/pull/145
.. _`#143`: https://github.com/lepture/flask-wtf/pull/143

Version 0.10.0
--------------

Released 2014/07/16

- Add configuration: WTF_CSRF_METHODS
- Support WTForms 2.0 now
- Fix csrf validation without time limit (time_limit=False)
- CSRF exempt supports blueprint `#111`_.

.. _`#111`: https://github.com/lepture/flask-wtf/issues/111

Version 0.9.5
-------------

Released 2014/03/21

- ``csrf_token`` for all template types `#112`_.
- Make FileRequired a subclass of InputRequired `#108`_.

.. _`#108`: https://github.com/lepture/flask-wtf/pull/108
.. _`#112`: https://github.com/lepture/flask-wtf/pull/112

Version 0.9.4
-------------

Released 2013/12/20

- Bugfix for csrf module when form has a prefix
- Compatible support for wtforms2
- Remove file API for FileField


Version 0.9.3
-------------

Released 2013/10/02

- Fix validation of recaptcha when app in testing mode `#89`_.
- Bugfix for csrf module `#91`_

.. _`#89`: https://github.com/lepture/flask-wtf/pull/89
.. _`#91`: https://github.com/lepture/flask-wtf/pull/91


Version 0.9.2
-------------

Released 2013/9/11

- Upgrade wtforms to 1.0.5.
- No lazy string for i18n `#77`_.
- No DateInput widget in html5 `#81`_.
- PUT and PATCH for CSRF `#86`_.

.. _`#77`: https://github.com/lepture/flask-wtf/issues/77
.. _`#81`: https://github.com/lepture/flask-wtf/issues/81
.. _`#86`: https://github.com/lepture/flask-wtf/issues/86


Version 0.9.1
-------------

Released 2013/8/21

This is a patch version for backward compitable for Flask<0.10 `#82`_.

.. _`#82`: https://github.com/lepture/flask-wtf/issues/82

Version 0.9.0
-------------

Released 2013/8/15

- Add i18n support (issue #65)
- Use default html5 widgets and fields provided by wtforms
- Python 3.3+ support
- Redesign form, replace SessionSecureForm
- CSRF protection solution
- Drop wtforms imports
- Fix recaptcha i18n support
- Fix recaptcha validator for python 3
- More test cases, it's 90%+ coverage now
- Redesign documentation

Version 0.8.4
-------------

Released 2013/3/28

- Recaptcha Validator now returns provided message (issue #66)
- Minor doc fixes
- Fixed issue with tests barking because of nose/multiprocessing issue.

Version 0.8.3
-------------

Released 2013/3/13

- Update documentation to indicate pending deprecation of WTForms namespace
  facade
- PEP8 fixes (issue #64)
- Fix Recaptcha widget (issue #49)

Version 0.8.2 and prior
-----------------------

Initial development by Dan Jacob and Ron Duplain. 0.8.2 and prior there was not
a change log.

