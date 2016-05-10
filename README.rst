Flask-WTF
=========

.. image:: https://img.shields.io/badge/flask-registered-green.svg?style=flat
   :target: https://github.com/pocoo/metaflask
   :alt: Meta Flask
.. image:: https://pypip.in/wheel/flask-wtf/badge.svg?style=flat
   :target: https://pypi.python.org/pypi/Flask-WTF/
   :alt: Wheel Status
.. image:: https://pypip.in/version/flask-wtf/badge.svg?style=flat
   :target: https://pypi.python.org/pypi/Flask-WTF/
   :alt: Latest Version
.. image:: https://travis-ci.org/lepture/flask-wtf.svg?branch=master
   :target: https://travis-ci.org/lepture/flask-wtf
   :alt: Travis CI Status
.. image:: https://coveralls.io/repos/lepture/flask-wtf/badge.svg?branch=master
   :target: https://coveralls.io/r/lepture/flask-wtf
   :alt: Coverage Status

Simple integration of Flask and WTForms, including CSRF, file upload, Recaptcha and are you a human integration.

For more information please refer to the online docs:

https://flask-wtf.readthedocs.org


This version was patch to support Are you a human from http://areyouahuman.com.

On the dashboard configuration from are you a human, you need to select game style : embedded.

You need to add : AYAH_PUBLISHER_KEY and AYAH_PUBLISHER_KEY to your flask conf.py for exemple.

Example
=======

In form.py

   from flask.ext.wtf import AreYouAHumanField
   
   [...]
   
   areyouahuman = AreYouAHumanField(_('Human ?'))
   
In your template with a macro jinja2 render_field

   {{ render_field(form.areyouahuman) }}
