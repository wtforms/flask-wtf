Quickstart
==========

Eager to get started? This page gives a good introduction to Flask-WTF.
It assumes you already have Flask-WTF installed. If you do not, head over
to the :doc:`install` section.


Creating Forms
--------------

Flask-WTF provides your Flask application integration with WTForms. For example::

    from flask_wtf import Form
    from wtforms import StringField
    from wtforms.validators import DataRequired

    class MyForm(Form):
        name = StringField('name', validators=[DataRequired()])


.. note::

   From version 0.9.0, Flask-WTF will not import anything from wtforms,
   you need to import fields from wtforms.

In addition, a CSRF token hidden field is created automatically. You can
render this in your template:

.. sourcecode:: html+jinja

    <form method="POST" action="/">
        {{ form.csrf_token }}
        {{ form.name.label }} {{ form.name(size=20) }}
        <input type="submit" value="Go">
    </form>

However, in order to create valid XHTML/HTML the Form class has a method
hidden_tag which renders any hidden fields, including the CSRF field,
inside a hidden DIV tag:

.. sourcecode:: html+jinja

    <form method="POST" action="/">
        {{ form.hidden_tag() }}
        {{ form.name.label }} {{ form.name(size=20) }}
        <input type="submit" value="Go">
    </form>


Validating Forms
----------------

Validating the request in your view handlers::

    @app.route('/submit', methods=('GET', 'POST'))
    def submit():
        form = MyForm()
        if form.validate_on_submit():
            return redirect('/success')
        return render_template('submit.html', form=form)

Note that you don't have to pass ``request.form`` to Flask-WTF; it will
load automatically. And the convenience ``validate_on_submit`` will check
if it is a POST request and if it is valid.

Heading over to :doc:`form` to learn more skills.
