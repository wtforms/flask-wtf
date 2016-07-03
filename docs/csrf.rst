CSRF Protection
===============

This part of the documentation covers the CSRF protection.

Why CSRF
--------

Flask-WTF form is already protecting you from CSRF, you don't have to
worry about that. However, you have views that contain no forms, and they
still need protection.

For example, the POST request is sent by AJAX, but it has no form behind
it. You can't get the csrf token prior 0.9.0 of Flask-WTF. That's why we
created this CSRF for you.

Implementation
--------------

.. module:: flask_wtf.csrf

To enable CSRF protection for all your view handlers, you need to enable
the :class:`CsrfProtect` module::

    from flask_wtf.csrf import CsrfProtect

    CsrfProtect(app)

Like any other Flask extensions, you can load it lazily::

    from flask_wtf.csrf import CsrfProtect

    csrf = CsrfProtect()

    def create_app():
        app = Flask(__name__)
        csrf.init_app(app)

.. note::

    You need to setup a secret key for CSRF protection. Usually, this
    is the same as your Flask app SECRET_KEY.

If the template has a form, you don't need to do any thing. It is the
same as before:

.. sourcecode:: html+jinja

    <form method="post" action="/">
        {{ form.csrf_token }}
    </form>

But if the template has no forms, you still need a csrf token:

.. sourcecode:: html+jinja

    <form method="post" action="/">
        <input type="hidden" name="csrf_token" value="{{ csrf_token() }}" />
    </form>

Whenever a CSRF validation fails, it will return a 400 response. You can
customize the error response::

    @csrf.error_handler
    def csrf_error(reason):
        return render_template('csrf_error.html', reason=reason), 400

We strongly suggest that you protect all your views with CSRF. But if
needed, you can exclude some views using a decorator::

    @csrf.exempt
    @app.route('/foo', methods=('GET', 'POST'))
    def my_handler():
        # ...
        return 'ok'

If needed, you can also exclude all the views from within a given Blueprint:

    csrf.exempt(account_blueprint)

You can also disable CSRF protection in all views by default, by setting
``WTF_CSRF_CHECK_DEFAULT`` to ``False``, and selectively call
``csrf.protect()`` only when you need. This also enables you to do some
pre-processing on the requests before checking for the CSRF token::

    @app.before_request
    def check_csrf():
        if not is_oauth(request):
            csrf.protect()

AJAX
----

Sending POST requests via AJAX is possible where there are no forms at all.
This feature is available since 0.9.0.

Assuming you have done ``CsrfProtect(app)``, you can get the csrf token via
``{{ csrf_token() }}``. This method is available in every template, that
way you don't have to worry if there are no forms for rendering the csrf token
field.

The suggested way is that you render the token in a ``<meta>`` tag:

.. sourcecode:: html+jinja

    <meta name="csrf-token" content="{{ csrf_token() }}">

And it is also possible to render it in the ``<script>`` tag:

.. sourcecode:: html+jinja

    <script type="text/javascript">
        var csrftoken = "{{ csrf_token() }}"
    </script>

We will take the ``<meta>`` way for example, the ``<script>`` way is far
more easier, you don't have to worry if there is no example for it.

Whenever you send a AJAX POST request, add the ``X-CSRFToken`` for it:

.. sourcecode:: javascript

    var csrftoken = $('meta[name=csrf-token]').attr('content')

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!/^(GET|HEAD|OPTIONS|TRACE)$/i.test(settings.type) && !this.crossDomain) {
                xhr.setRequestHeader("X-CSRFToken", csrftoken)
            }
        }
    })
