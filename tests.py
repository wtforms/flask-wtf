import re

from flask import Flask, Response
from flaskext.testing import TestCase
from flaskext.wtf import Form, TextField, Required

class TestCSRF(TestCase):

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

        return app

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
       
    def test_valid_csrf(self):

        response = self.client.get("/")
        pattern = re.compile(r'name="csrf" type="hidden" value="([0-9a-zA-Z-]*)"')
        match = pattern.search(response.data)
        assert match

        csrf_token = match.groups()[0]

        response = self.client.post("/", data={"name" : "danny", 
                                               "csrf" : csrf_token})

        print csrf_token, response.data
        assert "DANNY" in response.data


