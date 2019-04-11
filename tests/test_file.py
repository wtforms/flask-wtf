import pytest
import os
from werkzeug.datastructures import FileStorage, MultiDict
from wtforms import FileField as BaseFileField

from flask_wtf import FlaskForm
from flask_wtf._compat import FlaskWTFDeprecationWarning
from flask_wtf.file import FileAllowed, FileField, FileRequired, FileMaxSize


@pytest.fixture
def form(req_ctx):
    class UploadForm(FlaskForm):
        class Meta:
            csrf = False

        file = FileField()

    return UploadForm


def test_process_formdata(form):
    assert form(MultiDict((('file', FileStorage()),))).file.data is None
    assert form(
        MultiDict((('file', FileStorage(filename='real')),))
    ).file.data is not None


def test_file_required(form):
    form.file.kwargs['validators'] = [FileRequired()]

    f = form()
    assert not f.validate()
    assert f.file.errors[0] == 'This field is required.'

    f = form(file='not a file')
    assert not f.validate()
    assert f.file.errors[0] == 'This field is required.'

    f = form(file=FileStorage())
    assert not f.validate()

    f = form(file=FileStorage(filename='real'))
    assert f.validate()


def test_file_allowed(form):
    form.file.kwargs['validators'] = [FileAllowed(('txt',))]

    f = form()
    assert f.validate()

    f = form(file=FileStorage(filename='test.txt'))
    assert f.validate()

    f = form(file=FileStorage(filename='test.png'))
    assert not f.validate()
    assert f.file.errors[0] == 'File does not have an approved extension: txt'


def test_file_allowed_uploadset(app, form):
    pytest.importorskip('flask_uploads')
    from flask_uploads import UploadSet, configure_uploads

    app.config['UPLOADS_DEFAULT_DEST'] = 'uploads'
    txt = UploadSet('txt', extensions=('txt',))
    configure_uploads(app, (txt,))
    form.file.kwargs['validators'] = [FileAllowed(txt)]

    f = form()
    assert f.validate()

    f = form(file=FileStorage(filename='test.txt'))
    assert f.validate()

    f = form(file=FileStorage(filename='test.png'))
    assert not f.validate()
    assert f.file.errors[0] == 'File does not have an approved extension.'


def test_file_max_size_no_file_passes_validation(form):
    form.file.kwargs['validators'] = [FileMaxSize(180)]
    f = form()
    assert f.validate()


def test_file_max_size_small_file_passes_validation(form):
    form.file.kwargs['validators'] = [FileMaxSize(180)]

    test_file_smaller_than_max = open('small-file.test', "wb+")
    test_file_smaller_than_max.write(b"\0")
    test_file_smaller_than_max.seek(0)  # Reset file position

    f = form(file=FileStorage(stream=test_file_smaller_than_max))
    assert f.validate()
    test_file_smaller_than_max.close()
    os.remove('small-file.test')


def test_file_max_size_large_file_fails_validation(form):
    form.file.kwargs['validators'] = [FileMaxSize(180)]
    test_file_too_large = open('big-file.test', "wb+")
    test_file_too_large.seek(180 + 1)  # Create a file larger than the maximum size
    test_file_too_large.write(b"\0")
    test_file_too_large.seek(0)  # Reset file position

    f = form(file=FileStorage(stream=test_file_too_large))
    assert not f.validate()
    assert f.file.errors[0] == 'File must be smaller than 180 bytes.'
    test_file_too_large.close()
    os.remove('big-file.test')


def test_validate_base_field(req_ctx):
    class F(FlaskForm):
        class Meta:
            csrf = False

        f = BaseFileField(validators=[FileRequired()])

    assert not F().validate()
    assert not F(f=FileStorage()).validate()
    assert F(f=FileStorage(filename='real')).validate()


def test_deprecated_filefield(recwarn, form):
    assert not form().file.has_file()
    w = recwarn.pop(FlaskWTFDeprecationWarning)
    assert 'has_file' in str(w.message)
