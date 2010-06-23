from flask import Flask, render_template, flash, redirect, url_for
from flaskext.wtf import Form, TextField

class MyForm(Form):
    name = TextField("Name:")

app = Flask(__name__)
app.secret_key = "secret"
app.debug = True

@app.route("/", methods=("GET", "POST"))
def index():
    form = MyForm()
    if form.validate_on_submit():
        name = form.name.data
        flash("You entered %s" % name)
        return redirect(url_for("index"))
    return render_template("index.html", form=form)


if __name__ == "__main__":
    app.run()
