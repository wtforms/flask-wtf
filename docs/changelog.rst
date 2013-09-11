Flask-WTF Changelog
===================

Full list of changes between each Flask-WTF release.

Version 0.9.2
-------------

Released 2013/9/11

- Upgrade wtforms to 1.0.5.
- No lazy string for i18n `#77`_.
- No DateInput widget in html5 `#81`_.
- PUT and PATCH for CSRF `#86`_.

.. _`#77`: https://github.com/ajford/flask-wtf/issues/77
.. _`#81`: https://github.com/ajford/flask-wtf/issues/81
.. _`#86`: https://github.com/ajford/flask-wtf/issues/86


Version 0.9.1
-------------

Released 2013/8/21

This is a patch version for backward compitable for Flask<0.10 `#82`_.

.. _`#82`: https://github.com/ajford/flask-wtf/issues/82

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

