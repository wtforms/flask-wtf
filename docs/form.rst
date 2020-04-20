Creating Forms
==============

Secure Form
-----------

.. currentmodule:: flask_wtf

Without any configuration, the :class:`FlaskForm` will be a session secure
form with csrf protection. We encourage you do nothing.

But if you want to disable the csrf protection, you can pass::

    form = FlaskForm(meta={'csrf': False})

You can disable it globally—though you really shouldn't—with the
configuration::

    WTF_CSRF_ENABLED = False

In order to generate the csrf token, you must have a secret key, this
is usually the same as your Flask app secret key. If you want to use
another secret key, config it::

    WTF_CSRF_SECRET_KEY = 'a random string'


File Uploads
------------

.. currentmodule:: flask_wtf.file

The :class:`FileField` provided by Flask-WTF differs from the WTForms-provided
field. It will check that the file is a non-empty instance of
:class:`~werkzeug.datastructures.FileStorage`, otherwise ``data`` will be
``None``. ::

    from flask_wtf import FlaskForm
    from flask_wtf.file import FileField, FileRequired
    from werkzeug.utils import secure_filename

    class PhotoForm(FlaskForm):
        photo = FileField(validators=[FileRequired()])

    @app.route('/upload', methods=['GET', 'POST'])
    def upload():
        form = PhotoForm()

        if form.validate_on_submit():
            f = form.photo.data
            filename = secure_filename(f.filename)
            f.save(os.path.join(
                app.instance_path, 'photos', filename
            ))
            return redirect(url_for('index'))

        return render_template('upload.html', form=form)

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
:class:`FileRequired` and :class:`FileAllowed`. They can be used with both
Flask-WTF's and WTForms's ``FileField`` classes.

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

.. currentmodule:: flask_wtf.recaptcha

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
                        https://developers.google.com/recaptcha/docs/display#javascript_resource_apijs_parameters
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
