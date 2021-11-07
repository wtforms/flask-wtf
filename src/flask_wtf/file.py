from collections import abc

from werkzeug.datastructures import FileStorage
from wtforms import FileField as _FileField
from wtforms.validators import DataRequired
from wtforms.validators import StopValidation
from wtforms.validators import ValidationError


class FileField(_FileField):
    """Werkzeug-aware subclass of :class:`wtforms.fields.FileField`."""

    def process_formdata(self, valuelist):
        valuelist = (x for x in valuelist if isinstance(x, FileStorage) and x)
        data = next(valuelist, None)

        if data is not None:
            self.data = data
        else:
            self.raw_data = ()


class FileRequired(DataRequired):
    """Validates that the data is a Werkzeug
    :class:`~werkzeug.datastructures.FileStorage` object.

    :param message: error message

    You can also use the synonym ``file_required``.
    """

    def __call__(self, form, field):
        if not (isinstance(field.data, FileStorage) and field.data):
            raise StopValidation(
                self.message or field.gettext("This field is required.")
            )


file_required = FileRequired


class FileAllowed:
    """Validates that the uploaded file is allowed by a given list of
    extensions or a Flask-Uploads :class:`~flaskext.uploads.UploadSet`.

    :param upload_set: A list of extensions or an
        :class:`~flaskext.uploads.UploadSet`
    :param message: error message

    You can also use the synonym ``file_allowed``.
    """

    def __init__(self, upload_set, message=None):
        self.upload_set = upload_set
        self.message = message

    def __call__(self, form, field):
        if not (isinstance(field.data, FileStorage) and field.data):
            return

        filename = field.data.filename.lower()

        if isinstance(self.upload_set, abc.Iterable):
            if any(filename.endswith("." + x) for x in self.upload_set):
                return

            raise StopValidation(
                self.message
                or field.gettext(
                    "File does not have an approved extension: {extensions}"
                ).format(extensions=", ".join(self.upload_set))
            )

        if not self.upload_set.file_allowed(field.data, filename):
            raise StopValidation(
                self.message
                or field.gettext("File does not have an approved extension.")
            )


file_allowed = FileAllowed


class FileSize:
    """Validates that the uploaded file is within a minimum and maximum
    file size (set in bytes).

    :param min_size: minimum allowed file size (in bytes). Defaults to 0 bytes.
    :param max_size: maximum allowed file size (in bytes).
    :param message: error message

    You can also use the synonym ``file_size``.
    """

    def __init__(self, max_size, min_size=0, message=None):
        self.min_size = min_size
        self.max_size = max_size
        self.message = message

    def __call__(self, form, field):
        if not (isinstance(field.data, FileStorage) and field.data):
            return

        file_size = len(field.data.read())
        field.data.seek(0)  # reset cursor position to beginning of file

        if (file_size < self.min_size) or (file_size > self.max_size):
            # the file is too small or too big => validation failure
            raise ValidationError(
                self.message
                or field.gettext(
                    "File must be between {min_size} and {max_size} bytes.".format(
                        min_size=self.min_size, max_size=self.max_size
                    )
                )
            )


file_size = FileSize
