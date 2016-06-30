from __future__ import with_statement

from flask import Flask, render_template, jsonify
from wtforms import StringField, HiddenField, SubmitField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm
from flask_wtf._compat import text_type


def to_unicode(text):
    if not isinstance(text, text_type):
        return text.decode('utf-8')
    return text


class MyForm(FlaskForm):
    SECRET_KEY = "a poorly kept secret."
    name = StringField("Name", validators=[DataRequired()])
    submit = SubmitField("Submit")


class HiddenFieldsForm(FlaskForm):
    SECRET_KEY = "a poorly kept secret."
    name = HiddenField()
    url = HiddenField()
    method = HiddenField()
    secret = HiddenField()
    submit = SubmitField("Submit")

    def __init__(self, *args, **kwargs):
        super(HiddenFieldsForm, self).__init__(*args, **kwargs)
        self.method.name = '_method'


class SimpleForm(FlaskForm):
    SECRET_KEY = "a poorly kept secret."
    pass


class TestCase(object):
    def setUp(self):
        self.app = self.create_app()
        self.client = self.app.test_client()

    def create_app(self):
        app = Flask(__name__)
        app.secret_key = "secret"

        @app.route("/", methods=("GET", "POST"))
        def index():

            form = MyForm()
            if form.validate_on_submit():
                name = form.name.data.upper()
            else:
                name = ''

            return render_template("index.html",
                                   form=form,
                                   name=name)

        @app.route("/simple/", methods=("POST",))
        def simple():
            form = SimpleForm()
            form.validate()
            assert form.csrf_enabled
            assert not form.validate()
            return "OK"

        @app.route("/two_forms/", methods=("POST",))
        def two_forms():
            form = SimpleForm()
            assert form.csrf_enabled
            assert form.validate()
            assert form.validate()
            form2 = SimpleForm()
            assert form2.csrf_enabled
            assert form2.validate()
            return "OK"

        @app.route("/hidden/")
        def hidden():

            form = HiddenFieldsForm()
            return render_template("hidden.html", form=form)

        @app.route("/ajax/", methods=("POST",))
        def ajax_submit():
            form = MyForm()
            if form.validate_on_submit():
                return jsonify(name=form.name.data,
                               success=True,
                               errors=None)

            return jsonify(name=None,
                           #errors=form.errors,
                           success=False)

        return app
