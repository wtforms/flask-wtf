Flask-WTF
=========

.. image:: https://badge.fury.io/py/Flask-WTF.png
    :target: http://badge.fury.io/py/Flask-WTF
.. image:: https://travis-ci.org/lepture/flask-wtf.png?branch=master
    :target: https://travis-ci.org/lepture/flask-wtf
.. image:: https://coveralls.io/repos/lepture/flask-wtf/badge.png?branch=master
    :target: https://coveralls.io/r/lepture/flask-wtf

Simple integration of Flask and WTForms, including CSRF, file upload, Recaptcha and are you a human integration.

For more information please refer to the online docs:

https://flask-wtf.readthedocs.org


This version was patch to support Are you a human from http://areyouahuman.com.

You need to add : AYAH_PUBLISHER_KEY and AYAH_PUBLISHER_KEY to your flask conf.py for exemple.

Example
=======

In form.py

   from flask.ext.wtf import AreYouAHumanField
   
   [...]
   
   areyouahuman = AreYouAHumanField(_('Human ?'))
   
In your template with a macro jinja2 render_field

   {{ render_field(form.areyouahuman) }}
