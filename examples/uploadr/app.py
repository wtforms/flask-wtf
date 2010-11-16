from flask import Flask, render_template

from flaskext.wtf import Form, FileField

class FileUploadForm(Form):

    file_upload = FileField("File to upload")

DEBUG = True
SECRET_KEY = 'secret'

app = Flask(__name__)
app.config.from_object(__name__)

@app.route("/", methods=("GET", "POST",))
def index():

    form = FileUploadForm()

    if form.validate_on_submit():
        filedata = form.file_upload.file
    else:
        filedata = None

    return render_template("index.html", 
                           form=form, 
                           filedata=filedata)


if __name__ == "__main__":
    app.run()
