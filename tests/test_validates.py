from wtforms import StringField
from wtforms import TextAreaField
from wtforms.validators import DataRequired

from flask_wtf import FlaskForm
from flask_wtf import current_form
from flask_wtf import validates


class BasicForm(FlaskForm):
    name = StringField(validators=[DataRequired()])


def test_validates_with_form_class(app, client):
    @app.route("/", methods=["POST"])
    @validates(BasicForm)
    def index():
        assert current_form.name.data == "form"

    client.post("/", data=dict(name="form"))


def test_validates_with_form_class_and_fields(app, client):
    @app.route("/", methods=["POST"])
    @validates(BasicForm, text=TextAreaField("text"))
    def index():
        assert current_form.name.data == "name"
        assert current_form.text.data == "text"

    client.post("/", data=dict(name="name", text="text"))


def test_validates_with_fields_only(app, client):
    @app.route("/", methods=["POST"])
    @validates(name=StringField(validators=[DataRequired()]))
    def index():
        assert current_form.name.data == "name"

    client.post("/", data=dict(name="name"))
