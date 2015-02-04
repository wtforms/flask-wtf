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

In order to generate the csrf token, you must have a secret key, this
is usually the same as your Flask app secret key. If you want to use
another secret key, config it::

    WTF_CSRF_SECRET_KEY = 'a random string'


File Uploads
------------

.. module:: flask_wtf.file

Flask-WTF provides you a :class:`FileField` to handle file uploading,
it will automatically draw data from ``flask.request.files`` if the form
is posted. The ``data`` attribute of :class:`FileField` will be an
instance of Werkzeug FileStorage. 

For example::

    from werkzeug import secure_filename
    from flask_wtf.file import FileField

    class PhotoForm(Form):
        photo = FileField('Your photo')

    @app.route('/upload/', methods=('GET', 'POST'))
    def upload():
        form = PhotoForm()
        if form.validate_on_submit():
            filename = secure_filename(form.photo.data.filename)
            form.photo.data.save('uploads/' + filename)
        else:
            filename = None
        return render_template('upload.html', form=form, filename=filename)

.. note::

    Remember to set the ``enctype`` of your HTML form to
    ``multipart/form-data``, which means:

    .. sourcecode:: html

        <form action="/upload/" method="POST" enctype="multipart/form-data">
            ....
        </form>

More than that, Flask-WTF supports validation on file uploading. There
are :class:`FileRequired` and :class:`FileAllowed`.

The :class:`FileAllowed` works well with Flask-Uploads, for example::

    from flask.ext.uploads import UploadSet, IMAGES
    from flask_wtf import Form
    from flask_wtf.file import FileField, FileAllowed, FileRequired

    images = UploadSet('images', IMAGES)

    class UploadForm(Form):
        upload = FileField('image', validators=[
            FileRequired(),
            FileAllowed(images, 'Images only!')
        ])

It can work without Flask-Uploads too. You need to pass the extensions
to :class:`FileAllowed`::

    class UploadForm(Form):
        upload = FileField('image', validators=[
            FileRequired(),
            FileAllowed(['jpg', 'png'], 'Images only!')
        ])

HTML5 Widgets
-------------

.. note::

    HTML5 widgets and fields are builtin of wtforms since 1.0.5. You
    should consider import them from wtforms if possible.

    We will drop html5 module in next release 0.9.3.

You can import a number of HTML5 widgets from ``wtforms``::

    from wtforms.fields.html5 import URLField
    from wtforms.validators import url

    class LinkForm(Form):
        url = URLField(validators=[url()])


.. _recaptcha:

Recaptcha
---------

.. module:: flask_wtf.recaptcha

Flask-WTF also provides Recaptcha support through a :class:`RecaptchaField`::

    from flask_wtf import Form, RecaptchaField
    from wtforms import TextField

    class SignupForm(Form):
        username = TextField('Username')
        recaptcha = RecaptchaField()

This comes together with a number of configuration, which you have to
implement them.

===================== =========================================================
RECAPTCHA_PUBLIC_KEY  **required** A public key.
RECAPTCHA_PRIVATE_KEY **required** A private key.
RECAPTCHA_API_SERVER  **optional** Specify your Recaptcha API server.
RECAPTCHA_PARAMETERS  **optional** A dict of JavaScript (api.js) parameters.
RECAPTCHA_DATA_ATTRS  **optional** A dict of data attributes options.
                      https://developers.google.com/recaptcha/docs/display
===================== ==========================================================

Example of RECAPTCHA_PARAMETERS, and RECAPTCHA_DATA_ATTRS::

    RECAPTCHA_PARAMETERS = {'hl': 'zh', 'render': 'explicit'}
    RECAPTCHA_DATA_ATTRS = {'theme': 'dark'}

For testing your application, if ``app.testing`` is ``True``, recaptcha
field will always be valid for you convenience.

And it can be easily setup in the templates:

.. sourcecode:: html+jinja

    <form action="/" method="post">
        {{ form.username }}
        {{ form.recaptcha }}
    </form>

We have an example for you: `recaptcha@github`_.

.. _`recaptcha@github`: https://github.com/lepture/flask-wtf/tree/master/examples/recaptcha
