import warnings

from collections import Iterable
from werkzeug.datastructures import FileStorage
from wtforms import FileField as _FileField
from wtforms.validators import DataRequired, StopValidation

from flask_wtf._compat import FlaskWTFDeprecationWarning


class FileField(_FileField):
    """
    Werkzeug-aware subclass of **wtforms.FileField**

    .. deprecated:: 0.14
        ``has_file`` was simplified and merged into the validators.
        This subclass is no longer needed and will be removed in 1.0.
    """

    def __new__(cls, *args, **kwargs):
        warnings.warn(FlaskWTFDeprecationWarning(
            'The "FileField" subclass is no longer necessary and will be '
            'removed in 1.0. Use "wtforms.FileField" directly instead.'
        ), stacklevel=2)
        return super(FileField, cls).__new__(cls, *args, **kwargs)

    def has_file(self):
        """Return True if self.data is a
        :class:`~werkzeug.datastructures.FileStorage` object."""

        return isinstance(self.data, FileStorage)


class FileRequired(DataRequired):
    """Validates that the data is a Werkzeug
    :class:`~werkzeug.datastructures.FileStorage` object.

    :param message: error message

    You can also use the synonym ``file_required``.
    """

    def __call__(self, form, field):
        if not isinstance(field.data, FileStorage):
            if self.message is None:
                message = field.gettext('This field is required.')
            else:
                message = self.message

            raise StopValidation(message)

file_required = FileRequired


class FileAllowed(object):
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
        if not isinstance(field.data, FileStorage):
            return

        filename = field.data.filename.lower()

        if isinstance(self.upload_set, Iterable):
            if any(filename.endswith('.' + x) for x in self.upload_set):
                return

            raise StopValidation(self.message or field.gettext(
                'File does not have an approved extension: {extensions}'
            ).format(extensions=', '.join(self.upload_set)))

        if not self.upload_set.file_allowed(field.data, filename):
            raise StopValidation(self.message or field.gettext(
                'File does not have an approved extension.'
            ))

file_allowed = FileAllowed
