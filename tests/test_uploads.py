from __future__ import with_statement

from flask import render_template

from flaskext.uploads import UploadSet, IMAGES, TEXT, configure_uploads

from flaskext.wtf import Form, FileField, FieldList, \
                         file_required, file_allowed

from base import TestCase

images = UploadSet("images", IMAGES)
text = UploadSet("text", TEXT)

class FileUploadForm(Form):

    upload = FileField("Upload file")

class MultipleFileUploadForm(Form):

    uploads = FieldList(FileField("upload"), min_entries=3)


class ImageUploadForm(Form):

    upload = FileField("Upload file", 
                       validators=[file_required(),
                                   file_allowed(images)])

class TextUploadForm(Form):

    upload = FileField("Upload file", 
                       validators=[file_required(),
                                   file_allowed(text)])



class TestFileUpload(TestCase):

  
    def create_app(self):

        app = super(TestFileUpload, self).create_app()
        app.config['CSRF_ENABLED'] = False
        app.config['UPLOADED_FILES_DEST'] = 'uploads'
        app.config['UPLOADS_DEFAULT_DEST'] = 'uploads'
        configure_uploads(app, [images, text])

        @app.route("/upload-image/", methods=("POST",))
        def upload_image():
            form = ImageUploadForm()
            if form.validate_on_submit():
                return "OK"
            return "invalid"

        @app.route("/upload-text/", methods=("POST",))
        def upload_text():
            form = TextUploadForm()
            if form.validate_on_submit():
                return "OK"
            return "invalid"


        @app.route("/upload-multiple/", methods=("POST",))
        def upload_multiple():
            form = MultipleFileUploadForm()
            if form.validate_on_submit():
                assert len(form.uploads.entries) == 3
                for upload in form.uploads.entries:
                    assert upload.file is not None

            return "OK"

        @app.route("/upload/", methods=("POST",))
        def upload():
            form = FileUploadForm()
            if form.validate_on_submit():

                filedata = form.upload.file
            
            else:
                
                filedata = None

            return render_template("upload.html",
                                   filedata=filedata,
                                   form=form)
        
        return app

    def test_multiple_files(self):

        fps = [self.app.open_resource("flask.png") for i in xrange(3)]
        data = [("uploads-%d" % i, fp) for i, fp in enumerate(fps)] 
        response = self.client.post("/upload-multiple/", data=dict(data))
        assert response.status_code == 200

    def test_valid_file(self):
        
        with self.app.open_resource("flask.png") as fp:
            response = self.client.post("/upload-image/", 
                data={'upload' : fp})

        assert "OK" in response.data

    def test_missing_file(self):

        response = self.client.post("/upload-image/", 
                data={'upload' : "test"})

        assert "invalid" in response.data

    def test_invalid_file(self):

        with self.app.open_resource("flask.png") as fp:
            response = self.client.post("/upload-text/", 
                data={'upload' : fp})

        assert "invalid" in response.data


    def test_invalid_file_2(self):

        response = self.client.post("/upload/", 
                data={'upload' : 'flask.png'})

        assert "flask.png</h3>" not in response.data
