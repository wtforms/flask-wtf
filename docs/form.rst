Creating Forms
==============

Secure Form
-----------

.. module:: flask_wtf

Without any configuration, the :class:`FlaskForm` will be a session secure
form with csrf protection. We encourage you do nothing.

But if you want to disable the csrf protection, you can pass::

    form = FlaskForm(csrf_enabled=False)

You can disable it globally—though you really shouldn't—with the
configuration::

    WTF_CSRF_ENABLED = False

In order to generate the csrf token, you must have a secret key, this
is usually the same as your Flask app secret key. If you want to use
another secret key, config it::

    WTF_CSRF_SECRET_KEY = 'a random string'


File Uploads
------------

.. module:: flask_wtf.file

Flask-WTF provides :class:`FileField` to handle file uploading.
It automatically draws data from ``flask.request.files`` when the form
is posted. The field's ``data`` attribute is an instance of
:class:`~werkzeug.datastructures.FileStorage`. ::

    from werkzeug.utils import secure_filename
    from flask_wtf.file import FileField

    class PhotoForm(FlaskForm):
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

Remember to set the ``enctype`` of the HTML form to
``multipart/form-data``, otherwise ``request.files`` will be empty.

.. sourcecode:: html

    <form method="POST" enctype="multipart/form-data">
        ...
    </form>

Flask-WTF handles passing form data to the form for you.
If you pass in the data explicitly, remember that ``request.form`` must
be combined with ``request.files`` for the form to see the file data. ::

    form = PhotoForm()
    # is equivalent to:

    from flask import request
    from werkzeug.datastructures import CombinedMultiDict
    form = PhotoForm(CombinedMultiDict((request.files, request.form)))


Validation
~~~~~~~~~~

Flask-WTF supports validating file uploads with
:class:`FileRequired` and :class:`FileAllowed`.

:class:`FileAllowed` works well with Flask-Uploads. ::

    from flask_uploads import UploadSet, IMAGES
    from flask_wtf import FlaskForm
    from flask_wtf.file import FileField, FileAllowed, FileRequired

    images = UploadSet('images', IMAGES)

    class UploadForm(FlaskForm):
        upload = FileField('image', validators=[
            FileRequired(),
            FileAllowed(images, 'Images only!')
        ])

It can be used without Flask-Uploads by passing the extensions directly. ::

    class UploadForm(FlaskForm):
        upload = FileField('image', validators=[
            FileRequired(),
            FileAllowed(['jpg', 'png'], 'Images only!')
        ])


.. _recaptcha:

Recaptcha
---------

.. module:: flask_wtf.recaptcha

Flask-WTF also provides Recaptcha support through a :class:`RecaptchaField`::

    from flask_wtf import FlaskForm, RecaptchaField
    from wtforms import TextField

    class SignupForm(FlaskForm):
        username = TextField('Username')
        recaptcha = RecaptchaField()

This comes together with a number of configuration, which you have to
implement them.

======================= ==============================================
RECAPTCHA_PUBLIC_KEY    **required** A public key.
RECAPTCHA_PRIVATE_KEY   **required** A private key.
RECAPTCHA_API_SERVER    **optional** Specify your Recaptcha API server.
RECAPTCHA_PARAMETERS    **optional** A dict of JavaScript (api.js) parameters.
RECAPTCHA_DATA_ATTRS    **optional** A dict of data attributes options.
                        https://developers.google.com/recaptcha/docs/display
======================= ==============================================

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
