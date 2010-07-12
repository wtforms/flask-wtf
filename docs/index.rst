Flask-WTF
======================================

.. module:: Flask-WTF

**Flask-WTF** offers simple integration with `WTForms <http://wtforms.simplecodes.com/docs/0.6/>`_. This integration
includes optional CSRF handling for greater security.

Source code and issue tracking at `Bitbucket`_.

Installing Flask-WTF
---------------------

Install with **pip** and **easy_install**::

    pip install Flask-WTF

or download the latest version from Bitbucket::

    hg clone http://bitbucket.org/danjac/flask-wtf

    cd flask-wtf

    python setup.py develop

If you are using **virtualenv**, it is assumed that you are installing Flask-WTF
in the same virtualenv as your Flask application(s).

Configuring Flask-WTF
----------------------

The following settings are used with **Flask-WTF**:

    * ``CSRF_ENABLED`` default ``True``
    * ``CSRF_SESSION_KEY`` default ``_csrf_token``

``CSRF_ENABLED`` enables CSRF. You can disable by passing in the ``csrf_enabled`` parameter to your form::

    form = MyForm(csrf_enabled=False)

Generally speaking it's a good idea to enable CSRF. There are two situations where you might not want to:
unit tests and AJAX forms. In the first case, switching ``CSRF_ENABLED`` to ``False`` means that your
forms will still work (and the CSRF hidden field will still be printed) but no validation will be done. In the
second, CSRF validation is skipped if ``request.is_xhr`` is ``True`` (you can't do cross-domain AJAX anyway, 
so CSRF validation is redundant).

The ``CSRF_SESSION_KEY`` sets the key used in the Flask session for storing the generated token string. Usually
the default should suffice, in certain cases you might want a custom key (for example, having several forms in a
single page).

Both these settings can be overriden in the ``Form`` constructor by passing in ``csrf_enabled`` and ``csrf_session_key``
optional arguments respectively.

In addition, there are additional configuration settings required for Recaptcha integration : see below.

Creating forms
--------------

**Flask-WTF** provides you with all the API features of WTForms. For example::

    from flaskext.wtf import Form, TextField, Required

    class MyForm(Form):
        name = TextField(name, validators=[Required()])

In addition, a CSRF token hidden field is created. You can print this in your template as any other field::

    
    <form method="POST" action=".">
        {{ form.csrf }}
        {{ form.name.label }} {{ form.name(size=20) }}
        <input type="submit" value="Go">
    </form>

However, in order to create valid XHTML/HTML the ``Form`` class has a property, ``csrf_token``, which renders the field
inside a hidden DIV::
    
    <form method="POST" action=".">
        {{ form.csrf_token }}

File uploads
------------

The ``Form`` instance automatically appends a ``file`` attribute to any ``FileField`` field instances if the form is posted.

This ``file`` attribute is an instance of `Werkzeug FileStorage <http://werkzeug.pocoo.org/documentation/0.5.1/datastructures.html#werkzeug.FileStorage>`_ instance from ``request.files``.

For example::

    class PhotoForm(Form):

        photo = FileField("Your photo")

    @app.route("/upload/")
    def upload():
        form = PhotoForm()
        if form.validate_on_submit():
            filename = form.photo.file.filename
        else:
            filename = None

        return render_template("upload.html",
                               form=form,
                               filename=filename)

Remember to set the ``enctype`` of your HTML form to ``multipart/form-data`` to enable file uploads::

    <form action="." method="POST" enctype="multipart/form-data">
        ....
    </form>

Recaptcha
---------

**Flask-WTF** also provides Recaptcha support through a ``RecaptchaField``::
    
    from flaskext.wtf import Form, TextField, RecaptchaField

    class SignupForm(Form):
        username = TextField("Username")
        recaptcha = RecaptchaField()

This field handles all the nitty-gritty details of Recaptcha validation and output. The following settings 
are required in order to use Recaptcha:

    * ``RECAPTCHA_USE_SSL`` : default ``False``
    * ``RECAPTCHA_PUBLIC_KEY``
    * ``RECAPTCHA_PRIVATE_KEY``
    * ``RECAPTCHA_OPTIONS`` 

``RECAPTCHA_OPTIONS`` is an optional dict of configuration options. The public and private keys are required in
order to authenticate your request with Recaptcha - see `documentation <https://www.google.com/recaptcha/admin/create>`_ for details on how to obtain your keys.

If `flaskext-babel <http://packages.python.org/Flask-Babel/>`_ is installed then Recaptcha message strings can be localized.

API changes
-----------

The ``Form`` class provided by **Flask-WTF** is the same as for WTForms, but with a couple of changes. Aside from CSRF 
validation, a convenience method ``validate_on_submit`` is added::

    from flask import Flask, request, flash, redirect, url_for, \
        render_template
    
    from flaskext.wtf import Form, TextField

    app = Flask(__name__)

    class MyForm(Form):
        name = TextField("Name")

    @app.route("/submit/")
    def submit():
        
        form = MyForm()
        if form.validate_on_submit():
            flash("Success")
            redirect(url_for("index"))
        return render_template("index.html", form=form)

Note the difference from a pure WTForms solution::

    from flask import Flask, request, flash, redirect, url_for, \
        render_template

    from flaskext.wtf import Form, TextField

    app = Flask(__name__)

    class MyForm(Form):
        name = TextField("Name")

    @app.route("/submit/")
    def submit():
        
        form = MyForm(request.form)
        if request.method == "POST" and form.validate():
            flash("Success")
            redirect(url_for("index"))
        return render_template("index.html", form=form)

``validate_on_submit`` will automatically check if the request method is PUT or POST.

You don't need to pass ``request.form`` into your form instance, as the ``Form`` automatically populates from ``request.form`` unless
specified. Other arguments are as with ``wtforms.Form``.

.. _Flask: http://flask.pocoo.org
.. _Bitbucket: http://bitbucket.org/danjac/flask-wtf
