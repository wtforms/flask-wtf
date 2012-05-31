Flask-WTF
======================================

.. module:: Flask-WTF

**Flask-WTF** offers simple integration with `WTForms <http://wtforms.simplecodes.com/docs/>`_. This integration
includes optional CSRF handling for greater security.

Source code and issue tracking at `GitHub`_.

Installing Flask-WTF
---------------------

Install with **pip** and **easy_install**::

    pip install Flask-WTF

or download the latest version from version control::

    git clone https://github.com/rduplain/flask-wtf.git
    cd flask-wtf
    python setup.py develop

If you are using **virtualenv**, it is assumed that you are installing Flask-WTF
in the same virtualenv as your Flask application(s).

Configuring Flask-WTF
----------------------

The following settings are used with **Flask-WTF**:

    * ``CSRF_ENABLED`` default ``True``

``CSRF_ENABLED`` enables CSRF. You can disable by passing in the ``csrf_enabled`` parameter to your form::

    form = MyForm(csrf_enabled=False)

Generally speaking it's a good idea to enable CSRF. If you wish to disable checking in certain circumstances - for
example, in unit tests - you can set ``CSRF_ENABLED`` to **False** in your configuration.

CSRF support is built using ``wtforms.ext.csrf``; ``Form`` is a subclass of
`SessionSecureForm <http://wtforms.simplecodes.com/docs/dev/ext.html#wtforms.e
xt.csrf.session.SessionSecureForm>`_. Essentially, each form generates a CSRF
token deterministically based on a secret key and a randomly generated value
stored in the user's session. You can specify a secret key by passing a value
to the ``secret_key`` parameter of the form constructor, setting a
``SECRET_KEY`` variable on a form class, or setting the config variable
``SECRET_KEY``; if none of these are present, ``app.secret_key`` will be used
(if this is also not present, then CSRF is impossible; creating a form with
``csrf_enabled = True`` will raise an exception).

**NOTE:** Previous to version **0.5.2**, **Flask-WTF** automatically skipped CSRF validation in the case of AJAX
POST requests, as AJAX toolkits added headers such as ``X-Requested-With`` when using the XMLHttpRequest and browsers
enforced a strict same-origin policy.

However it has since come to light that various browser plugins can circumvent these measures, rendering AJAX requests
insecure by allowing forged requests to appear as an AJAX request.

Therefore CSRF checking will now be applied to all POST requests, unless you disable CSRF at your own risk through the options
described above.

You can pass in the CSRF field manually in your AJAX request by accessing the **csrf** field in your form directly::

    var params = {'csrf' : '{{ form.csrf_token }}'};

A more complete description of the issue can be found `here <http://www.djangoproject.com/weblog/2011/feb/08/security/>`_.


In addition, there are additional configuration settings required for Recaptcha integration : see below.

Creating forms
--------------

**Flask-WTF** provides you with all the API features of WTForms. For example::

    from flaskext.wtf import Form, TextField, Required

    class MyForm(Form):
        name = TextField(name, validators=[Required()])

In addition, a CSRF token hidden field is created. You can print this in your template as any other field::

    
    <form method="POST" action=".">
        {{ form.csrf_token }}
        {{ form.name.label }} {{ form.name(size=20) }}
        <input type="submit" value="Go">
    </form>

.. warning::
    .. versionchanged:: 0.6
        The csrf field renamed from ``csrf`` to ``csrf_token``.

However, in order to create valid XHTML/HTML the ``Form`` class has a method ``hidden_tag`` which renders any
hidden fields, including the CSRF field, inside a hidden DIV tag::
    
    <form method="POST" action=".">
        {{ form.hidden_tag() }}

Using the 'safe' filter
-----------------------

The **safe** filter used to be required with WTForms in Jinja2 templates, otherwise your markup would be escaped. For example:

    {{ form.name|safe }}

However widgets in the latest version of WTForms return a `HTML safe string <http://jinja.pocoo.org/2/documentation/api#jinja2.Markup>`_ so you shouldn't need to use **safe**.

Ensure you are running the latest stable version of WTForms so that you don't need to use this filter everywhere.

File uploads
------------

Instances of the field type ``FileField`` automatically draw data from ``flask.request.files`` if the form is posted.

The ``data`` attribute will be an instance of `Werkzeug FileStorage <http://werkzeug.pocoo.org/documentation/0.5.1/datastructures.html#werkzeug.FileStorage>`_.

For example::

    from werkzeug import secure_filename

    class PhotoForm(Form):

        photo = FileField("Your photo")

    @app.route("/upload/", methods=("GET", "POST"))
    def upload():
        form = PhotoForm()
        if form.validate_on_submit():
            filename = secure_filename(form.photo.data.filename)
        else:
            filename = None

        return render_template("upload.html",
                               form=form,
                               filename=filename)

It's recommended you use **werkzeug.secure_filename** on any uploaded files as shown in the example to prevent malicious attempts to access your filesystem.

Remember to set the ``enctype`` of your HTML form to ``multipart/form-data`` to enable file uploads::

    <form action="." method="POST" enctype="multipart/form-data">
        ....
    </form>

**Note:**  as of version **0.4** all **FileField** instances have access to the corresponding **FileStorage** object
in **request.files**, including those embedded in **FieldList** instances.


Validating file uploads
-----------------------

**Flask-WTF** supports validation through the `Flask Uploads <http://packages.python.org/Flask-Uploads/>`_ extension. If you use this (highly recommended) extension you can use it to add validation to your file fields. For example::


    from flaskext.uploads import UploadSet, IMAGES
    from flaskext.wtf import Form, FileField, file_allowed, \
        file_required

    images = UploadSet("images", IMAGES)

    class UploadForm(Form):

        upload = FileField("Upload your image", 
                           validators=[file_required(),
                                       file_allowed(images, "Images only!")])

In the above example, only image files (JPEGs, PNGs etc) can be uploaded. The **file_required** validator, which does not require **Flask-Uploads**, will raise a validation error if the field does not contain a **FileStorage** object.


HTML5 widgets
-------------

**Flask-WTF** supports a number of HTML5 widgets. Of course, these widgets must be supported by your target browser(s) in order to be properly used.

HTML5-specific widgets are available under the **flaskext.wtf.html5** package::

    from flaskext.wtf.html5 import URLField

    class LinkForm():

        url = URLField(validators=[url()])

See the `API`_ for more details.

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

Under test conditions (i.e. Flask app ``testing`` is ``True``) Recaptcha will always validate - this is because it's hard to know the correct Recaptcha image when running tests. Bear in mind that you need to pass the data to `recaptcha_challenge_field` and `recaptcha_response_field`, not `recaptcha`::

    response = self.client.post("/someurl/", data={
                                'recaptcha_challenge_field' : 'test',
                                'recaptcha_response_field' : 'test'})

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

    @app.route("/submit/", methods=("GET", "POST"))
    def submit():
        
        form = MyForm()
        if form.validate_on_submit():
            flash("Success")
            return redirect(url_for("index"))
        return render_template("index.html", form=form)

Note the difference from a pure WTForms solution::

    from flask import Flask, request, flash, redirect, url_for, \
        render_template

    from flaskext.wtf import Form, TextField

    app = Flask(__name__)

    class MyForm(Form):
        name = TextField("Name")

    @app.route("/submit/", methods=("GET", "POST"))
    def submit():
        
        form = MyForm(request.form)
        if request.method == "POST" and form.validate():
            flash("Success")
            return redirect(url_for("index"))
        return render_template("index.html", form=form)

``validate_on_submit`` will automatically check if the request method is PUT or POST.

You don't need to pass ``request.form`` into your form instance, as the ``Form`` automatically populates from ``request.form`` unless alternate data is specified. Pass in ``None`` to suppress this. Other arguments are as with ``wtforms.Form``.

API
---

.. module:: flaskext.wtf

.. autoclass:: Form
   :members:
    
.. autoclass:: RecaptchaField

.. autoclass:: Recaptcha

.. autoclass:: RecaptchaWidget

.. module:: flaskext.wtf.file

.. autoclass:: FileField
   :members:

.. autoclass:: FileAllowed

.. autoclass:: FileRequired

.. module:: flaskext.wtf.html5

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



.. _Flask: http://flask.pocoo.org
.. _GitHub: http://github.com/rduplain/flask-wtf
