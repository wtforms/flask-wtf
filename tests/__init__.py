from __future__ import with_statement

import re

from flask import Flask, Response, render_template, jsonify
from flaskext.uploads import UploadSet, IMAGES, TEXT, configure_uploads
from flaskext.testing import TestCase as _TestCase
from flaskext.wtf import Form, TextField, FileField, HiddenField, \
        SubmitField, Required, FieldList, file_required, file_allowed, html5

class DummyField(object):
    def __init__(self, data, name='f', label='', id='', type='TextField'):
        self.data = data
        self.name = name
        self.label = label
        self.id = id
        self.type = type

    _value       = lambda x: x.data
    __unicode__  = lambda x: x.data
    __call__     = lambda x, **k: x.data
    __iter__     = lambda x: iter(x.data)
    iter_choices = lambda x: iter(x.data)


class TestCase(_TestCase):
    
    def create_app(self):
        
        class MyForm(Form):
            name = TextField("Name", validators=[Required()])
            submit = SubmitField("Submit")

        class HiddenFieldsForm(Form):
            name = HiddenField()
            url = HiddenField()
            method = HiddenField()
            secret = HiddenField()
            submit = SubmitField("Submit")

            def __init__(self, *args, **kwargs):
                super(HiddenFieldsForm, self).__init__(*args, **kwargs)
                self.method.name = '_method'

        class SimpleForm(Form):
            pass

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
            assert not form.validate()
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
                           errors=form.errors,
                           success=False)

        
        return app

class HTML5Tests(TestCase):

    field = DummyField("name", id="name", name="name")

    def test_url_input(self):

        assert html5.URLInput()(self.field) == \
        '<input id="name" name="name" type="url" value="name" />'
 
    def test_search_input(self):

        assert html5.SearchInput()(self.field) == \
        '<input id="name" name="name" type="search" value="name" />'
         
    def test_date_input(self):

        assert html5.DateInput()(self.field) == \
        '<input id="name" name="name" type="date" value="name" />'
 
    def test_email_input(self):

        assert html5.EmailInput()(self.field) == \
        '<input id="name" name="name" type="email" value="name" />'
     
    def test_number_input(self):

        assert html5.NumberInput()(self.field, min=0, max=10) == \
        '<input id="name" max="10" min="0" name="name" type="number" value="name" />'
     
    def test_range_input(self):

        assert html5.RangeInput()(self.field, min=0, max=10) == \
        '<input id="name" max="10" min="0" name="name" type="range" value="name" />'
 
# FILE UPLOAD TESTS #

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

        @app.route("/upload-multiple-field/", methods=("POST",))
        def upload_multiple_field():
            form = MultipleFileFieldUploadForm()
            if form.validate_on_submit():
                assert len(form.uploads.files) == 3
                for upload in form.uploads.files:
                    assert "flask.png" in upload.filename
                
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


    def test_invalid_file(self):
        
        response = self.client.post("/upload/", 
                data={'upload' : 'flask.png'})

        assert "flask.png</h3>" not in response.data

class TestValidateOnSubmit(TestCase):

    def test_not_submitted(self):

        response = self.client.get("/")
        assert 'DANNY' not in response.data

    def test_submitted_not_valid(self):

        self.app.config['CSRF_ENABLED'] = False

        response = self.client.post("/", data={})

        assert 'DANNY' not in response.data

    def test_submitted_and_valid(self):
        
        self.app.config['CSRF_ENABLED'] = False

        response = self.client.post("/", data={"name" : "danny"})
        print response.data

        assert 'DANNY' in response.data


class TestHiddenTag(TestCase):

    def test_hidden_tag(self):

        response = self.client.get("/hidden/")
        assert response.data.count('type="hidden"') == 5
        assert 'name="_method"' in response.data


class TestCSRF(TestCase):

    def test_csrf_token(self):

        response = self.client.get("/")
        assert '<div style="display:none;"><input id="csrf" name="csrf" type="hidden" value' in response.data
    
    def test_invalid_csrf(self):

        response = self.client.post("/", data={"name" : "danny"})
        assert 'DANNY' not in response.data
        assert "Missing or invalid CSRF token" in response.data

    def test_csrf_disabled(self):
        
        self.app.config['CSRF_ENABLED'] = False

        response = self.client.post("/", data={"name" : "danny"})
        assert 'DANNY' in response.data

    def test_validate_twice(self):

        response = self.client.post("/simple/", data={})
        self.assert_200(response)

    def test_ajax(self):

        response = self.client.post("/ajax/", 
                                    data={"name" : "danny"},
                                    headers={'X-Requested-With' : 'XMLHttpRequest'})
        
        assert response.status_code == 200

    def test_valid_csrf(self):

        response = self.client.get("/")
        pattern = re.compile(r'name="csrf" type="hidden" value="([0-9a-zA-Z-]*)"')
        match = pattern.search(response.data)
        assert match

        csrf_token = match.groups()[0]

        response = self.client.post("/", data={"name" : "danny", 
                                               "csrf" : csrf_token})

        assert "DANNY" in response.data

