from flask import Flask, render_template, flash, session, redirect, url_for
from flaskext.wtf import Form, TextAreaField, RecaptchaField

DEBUG = True
SECRET_KEY = 'secret'

RECAPTCHA_PUBLIC_KEY = '6LeSIrsSAAAAAHDr5cU_6i1JWVpmlMo6dCruY6gp'
RECAPTCHA_PRIVATE_KEY = '6LeSIrsSAAAAANXeS29Eet5NfzNWhVFCrtJu9M4g'

app = Flask(__name__)
app.config.from_object(__name__)

class CommentForm(Form):
    
    comment = TextAreaField("Comment")
    recaptcha = RecaptchaField()

@app.route("/")
def index(form=None):
    if form is None:
        form = CommentForm()
    comments = session.get("comments", [])
    return render_template("index.html", 
                           comments=comments,
                           form=form)

@app.route("/add/", methods=("POST",))
def add_comment():

    form = CommentForm()
    if form.validate_on_submit():
        comments = session.pop('comments', [])
        comments.append(form.comment.data)
        session['comments'] = comments
        flash("You have added a new comment")
        return redirect(url_for("index"))
    return index(form)
    

if __name__ == "__main__":
    app.run()
