# -*- coding: utf-8 -*-
"""
    Flaskr
    ~~~~~~

    A microblog example application written as Flask tutorial with
    Flask using flask-sqlalchemy and flask-wtf extensions.

    Adapted from original (c) Armin Ronacher.

    :copyright: (c) 2010 by Dan Jacob.
    :license: BSD, see LICENSE for more details.
"""
from __future__ import with_statement
from flask import (Flask, session, redirect, url_for, abort,
                   render_template, flash)
from flask.ext.wtf import Form
from wtforms import TextField, TextAreaField, PasswordField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from flask.ext.sqlalchemy import SQLAlchemy

# configuration
DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///flaskr.db'
SQLALCHEMY_ECHO = DEBUG
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)

db = SQLAlchemy(app)


class Entry(db.Model):

    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Unicode(200))
    text = db.Column(db.UnicodeText)

db.create_all()


class EntryForm(Form):

    title = TextField("Title", validators=[DataRequired()])
    text = TextAreaField("Text")
    submit = SubmitField("Share")


class LoginForm(Form):

    username = TextField("Username")
    password = PasswordField("Password")
    submit = SubmitField("Login")

    def validate_username(self, field):
        if field.data != USERNAME:
            raise ValidationError("Invalid username")

    def validate_password(self, field):
        if field.data != PASSWORD:
            raise ValidationError("Invalid password")


@app.route('/')
def show_entries():
    entries = Entry.query.order_by(Entry.id.desc())
    form = EntryForm()
    return render_template('show_entries.html', entries=entries, form=form)


@app.route('/add', methods=['POST'])
def add_entry():
    if not session.get('logged_in'):
        abort(401)

    form = EntryForm()
    if form.validate():
        entry = Entry()
        form.populate_obj(entry)
        db.session.add(entry)
        db.session.commit()
        flash('New entry was successfully posted')
    else:
        flash("Your form contained errors")

    return redirect(url_for('show_entries'))


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session['logged_in'] = True
        flash('You were logged in')
        return redirect(url_for('show_entries'))
    return render_template('login.html', form=form)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('show_entries'))


if __name__ == '__main__':
    db.create_all()
    app.run()
