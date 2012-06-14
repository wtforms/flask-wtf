from __future__ import with_statement

from StringIO import StringIO

from flask import render_template, request

from flask.ext.uploads import UploadSet, IMAGES, TEXT, configure_uploads

from flask.ext.wtf import Form, TextField, FileField, FieldList, \
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
                    assert upload.has_file()

            return "OK"

        @app.route("/upload/", methods=("POST",))
        def upload():
            form = FileUploadForm()
            if form.validate_on_submit():
                filedata = form.upload.data
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
                data={'upload': fp})

        assert "OK" in response.data

    def test_missing_file(self):
        response = self.client.post("/upload-image/",
                data={'upload': "test"})

        assert "invalid" in response.data

    def test_invalid_file(self):
        with self.app.open_resource("flask.png") as fp:
            response = self.client.post("/upload-text/", 
                data={'upload': fp})

        assert "invalid" in response.data

    def test_invalid_file_2(self):
        response = self.client.post("/upload/",
                data={'upload': 'flask.png'})

        assert "flask.png</h3>" not in response.data


class BrokenForm(Form):
    text_fields = FieldList(TextField())
    file_fields = FieldList(FileField())

text_data = [('text_fields-0', 'First input'),
             ('text_fields-1', 'Second input')]

file_data = [('file_fields-0', (StringIO('contents 0'), 'file0.txt')),
             ('file_fields-1', (StringIO('contents 1'), 'file1.txt'))]

class TestFileList(TestCase):
    def test_multiple_upload(self):
        with self.app.test_request_context(method='POST',
                                           data=dict(text_data + file_data)):
            assert len(request.files) # the files have been added to the
                                      # request

            f = BrokenForm(csrf_enabled=False)

            assert f.validate_on_submit()
            assert len(text_data) == len(f.text_fields)
            assert len(file_data) == len(f.file_fields)
