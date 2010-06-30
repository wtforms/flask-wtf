import re
import unittest

from flask import Flask, Response, jsonify
from flaskext.wtf import Form, TextField, Required

class TestCase(unittest.TestCase):
    
    def create_app(self):
        
        class MyForm(Form):
            name = TextField("Name", validators=[Required()])

        app = Flask(__name__)
        app.secret_key = "secret"
        
        @app.route("/", methods=("GET", "POST"))
        def index():
            
            form = MyForm()
            if form.validate_on_submit():
                name = form.name.data
            else:
                name = ''
            
            return Response("""
            <html>
                <body>
                    %s
                    %s
                    <form method="POST" action=".">
                        %s
                        <p>
                           %s %s
                        </p>
                    </form>
                </body>
            </html>
            """ %(
                name.upper(),
                form.errors,
                form.csrf_token,
                form.name.label,
                form.name
            ))

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

    def __call__(self, result=None):
        """
        Does the required setup, doing it here
        means you don't have to call super.setUp
        in subclasses.
        """
        self._pre_setup()
        super(TestCase, self).__call__(result)
        self._post_tearDown()

    def _pre_setup(self):
        self.app = self.create_app()
        self.client = self.app.test_client()
       
        # now you can use flask thread locals

        self._ctx = self.app.test_request_context()
        self._ctx.push()

    def _post_tearDown(self):
        self._ctx.pop()

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

        assert 'DANNY' in response.data


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

