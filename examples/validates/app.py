from flask import Flask
from flask import render_template
from flask_wtf import current_form
from flask_wtf import validates
from wtforms import StringField
from wtforms import SubmitField
from wtforms import TextAreaField
from wtforms.validators import DataRequired


DEBUG = True
SECRET_KEY = "secret"

app = Flask(__name__)
app.config.from_object(__name__)


@app.route("/", methods=("GET", "POST",))
@validates(title=StringField("Title", validators=[DataRequired()]),
           text=TextAreaField("Text"),
           submit=SubmitField("Create"))
def index():
    return render_template("index.html", form=current_form)


if __name__ == "__main__":
    app.run()
