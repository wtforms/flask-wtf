import pytest
from werkzeug.datastructures import FileStorage
from werkzeug.datastructures import MultiDict
from wtforms import FileField as BaseFileField

from flask_wtf import FlaskForm
from flask_wtf.file import FileAllowed
from flask_wtf.file import FileField
from flask_wtf.file import FileRequired
from flask_wtf.file import FileSize


@pytest.fixture
def form(req_ctx):
    class UploadForm(FlaskForm):
        class Meta:
            csrf = False

        file = FileField()

    return UploadForm


def test_process_formdata(form):
    assert form(MultiDict((("file", FileStorage()),))).file.data is None
    assert (
        form(MultiDict((("file", FileStorage(filename="real")),))).file.data is not None
    )


def test_file_required(form):
    form.file.kwargs["validators"] = [FileRequired()]

    f = form()
    assert not f.validate()
    assert f.file.errors[0] == "This field is required."

    f = form(file="not a file")
    assert not f.validate()
    assert f.file.errors[0] == "This field is required."

    f = form(file=FileStorage())
    assert not f.validate()

    f = form(file=FileStorage(filename="real"))
    assert f.validate()


def test_file_allowed(form):
    form.file.kwargs["validators"] = [FileAllowed(("txt",))]

    f = form()
    assert f.validate()

    f = form(file=FileStorage(filename="test.txt"))
    assert f.validate()

    f = form(file=FileStorage(filename="test.png"))
    assert not f.validate()
    assert f.file.errors[0] == "File does not have an approved extension: txt"


def test_file_allowed_uploadset(app, form):
    pytest.importorskip("flask_uploads")
    from flask_uploads import UploadSet, configure_uploads

    app.config["UPLOADS_DEFAULT_DEST"] = "uploads"
    txt = UploadSet("txt", extensions=("txt",))
    configure_uploads(app, (txt,))
    form.file.kwargs["validators"] = [FileAllowed(txt)]

    f = form()
    assert f.validate()

    f = form(file=FileStorage(filename="test.txt"))
    assert f.validate()

    f = form(file=FileStorage(filename="test.png"))
    assert not f.validate()
    assert f.file.errors[0] == "File does not have an approved extension."


def test_file_size_no_file_passes_validation(form):
    form.file.kwargs["validators"] = [FileSize(max_size=100)]
    f = form()
    assert f.validate()


def test_file_size_small_file_passes_validation(form, tmp_path):
    form.file.kwargs["validators"] = [FileSize(max_size=100)]
    path = tmp_path / "test_file_smaller_than_max.txt"
    path.write_bytes(b"\0")

    with path.open("rb") as file:
        f = form(file=FileStorage(file))
        assert f.validate()


@pytest.mark.parametrize(
    "min_size, max_size, invalid_file_size", [(1, 100, 0), (0, 100, 101)]
)
def test_file_size_invalid_file_size_fails_validation(
    form, min_size, max_size, invalid_file_size, tmp_path
):
    form.file.kwargs["validators"] = [FileSize(min_size=min_size, max_size=max_size)]
    path = tmp_path / "test_file_invalid_size.txt"
    path.write_bytes(b"\0" * invalid_file_size)

    with path.open("rb") as file:
        f = form(file=FileStorage(file))
        assert not f.validate()
        assert f.file.errors[
            0
        ] == "File must be between {min_size} and {max_size} bytes.".format(
            min_size=min_size, max_size=max_size
        )


def test_validate_base_field(req_ctx):
    class F(FlaskForm):
        class Meta:
            csrf = False

        f = BaseFileField(validators=[FileRequired()])

    assert not F().validate()
    assert not F(f=FileStorage()).validate()
    assert F(f=FileStorage(filename="real")).validate()
