from __future__ import with_statement

try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO

from flask import render_template, request

from wtforms import StringField, FieldList
from flask_wtf import FlaskForm
from flask_wtf.file import FileField
from flask_wtf.file import file_required, file_allowed

from .base import TestCase


class UploadSet(object):
    def __init__(self, name='files', extensions=None):
        self.name = name
        self.extensions = extensions

    def file_allowed(self, storage, basename):
        if not self.extensions:
            return True

        ext = basename.rsplit('.', 1)[-1]
        return ext in self.extensions

images = UploadSet('images', ['jpg', 'png'])


class FileUploadForm(FlaskForm):
    upload = FileField("Upload file")


class MultipleFileUploadForm(FlaskForm):
    uploads = FieldList(FileField("upload"), min_entries=3)


class ImageUploadForm(FlaskForm):
    upload = FileField("Upload file",
                       validators=[file_required(),
                                   file_allowed(images)])


class TextUploadForm(FlaskForm):
    upload = FileField("Upload file",
                       validators=[file_required(),
                                   file_allowed(['txt'])])


class TestFileUpload(TestCase):
    def create_app(self):
        app = super(TestFileUpload, self).create_app()
        app.config['WTF_CSRF_ENABLED'] = False

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
        fps = [self.app.open_resource("flask.png") for i in range(3)]
        data = [("uploads-%d" % i, fp) for i, fp in enumerate(fps)]
        response = self.client.post("/upload-multiple/", data=dict(data))
        assert response.status_code == 200

    def test_valid_file(self):
        with self.app.open_resource("flask.png") as fp:
            response = self.client.post(
                "/upload-image/",
                data={'upload': fp}
            )

        assert b'OK' in response.data

    def test_missing_file(self):
        response = self.client.post(
            "/upload-image/",
            data={'upload': "test"}
        )

        assert b'invalid' in response.data

    def test_invalid_file(self):
        with self.app.open_resource("flask.png") as fp:
            response = self.client.post(
                "/upload-text/",
                data={'upload': fp}
            )

        assert b'invalid' in response.data

    def test_invalid_file_2(self):
        response = self.client.post(
            "/upload/",
            data={'upload': 'flask.png'}
        )

        assert b'flask.png</h3>' not in response.data

    def test_valid_txt_file(self):
        with self.app.open_resource("flask.txt") as fp:
            response = self.client.post(
                "/upload-text/",
                data={'upload': fp}
            )

        assert b'OK' in response.data

    def test_invalid_image_file(self):
        with self.app.open_resource("flask.txt") as fp:
            response = self.client.post(
                "/upload-image/",
                data={'upload': fp}
            )

        assert b'invalid' in response.data


class BrokenForm(FlaskForm):
    text_fields = FieldList(StringField())
    file_fields = FieldList(FileField())

text_data = [('text_fields-0', 'First input'),
             ('text_fields-1', 'Second input')]

file_data = [('file_fields-0', (BytesIO(b'contents 0'), 'file0.txt')),
             ('file_fields-1', (BytesIO(b'contents 1'), 'file1.txt'))]


class TestFileList(TestCase):
    def test_multiple_upload(self):
        data = dict(text_data + file_data)
        with self.app.test_request_context(method='POST', data=data):
            assert len(request.files)  # the files have been added to the
                                       # request

            f = BrokenForm(csrf_enabled=False)

            assert f.validate_on_submit()
            assert len(text_data) == len(f.text_fields)
            assert len(file_data) == len(f.file_fields)
