flask-wtf
======================================

.. module:: flask-wtf

Flask-WTF offers simple integration with `WTForms <http://wtforms.simplecodes.com/docs/0.6/>`_. This integration
includes optional CSRF handling for greater security.

Source code and issue tracking at `Bitbucket`_.

Installing flask-wtf
---------------------

Install with **pip** and **easy_install**::

    pip install Flask-WTF

or download the latest version from Bitbucket::

    hg clone http://bitbucket.org/danjac/flask-wtf

    cd flask-wtf

    python setup.py install

If you are using **virtualenv**, it is assumed that you are installing flask-mail
in the same virtualenv as your Flask application(s).

Configuring flask-wtf
----------------------

The following settings are used with flask-wtf:

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

Creating forms
--------------

Flask-WTF provides you with all the API features of WTForms. For example::

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


API changes
-----------

The ``Form`` class provided by Flask-WTF is the same as for WTForms, but with a couple of changes. Aside from CSRF 
validation, a convenience method ``validate_on_submit`` is added::

    @app.route("/submit/")
    def submit():
        
        form = MyForm()
        if form.validate_on_submit():
            flash("Success")
            redirect(url_for("index"))
        return render_template("index.html", form=form)

Note the difference from a pure WTForms solution::

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
