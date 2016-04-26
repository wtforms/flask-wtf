from werkzeug import FileStorage
from wtforms import FileField as _FileField
from wtforms.validators import InputRequired, StopValidation


class FileField(_FileField):
    """
    Werkzeug-aware subclass of **wtforms.FileField**

    Provides a `has_file()` method to check if its data is a FileStorage
    instance with an actual file.
    """
    def has_file(self):
        '''Return True iff self.data is a FileStorage with file data'''
        if not isinstance(self.data, FileStorage):
            return False
        # filename == None => the field was present but no file was entered
        # filename == '<fdopen>' is for a werkzeug hack:
        #   large file uploads will get stored in a temporary file on disk and
        #   show up as an extra FileStorage with name '<fdopen>'
        return self.data.filename not in [None, '', '<fdopen>']


class FileRequired(InputRequired):
    """
    Validates that field has a file.

    :param message: error message

    You can also use the synonym **file_required**.
    """

    def __call__(self, form, field):
        if not field.has_file():
            if self.message is None:
                message = field.gettext('This field is required.')
            else:
                message = self.message
            raise StopValidation(message)

file_required = FileRequired


class FileAllowed(object):
    """
    Validates that the uploaded file is allowed by the given
    Flask-Uploads UploadSet.

    :param upload_set: A list/tuple of extention names or an instance
                       of ``flask_uploads.UploadSet``
    :param message: error message

    You can also use the synonym **file_allowed**.
    """

    def __init__(self, upload_set, message=None):
        self.upload_set = upload_set
        self.message = message

    def __call__(self, form, field):
        if not field.has_file():
            return

        filename = field.data.filename.lower()

        if isinstance(self.upload_set, (tuple, list)):
            if any(filename.endswith('.' + x) for x in self.upload_set):
                return
            message = (
                'File does not end with any of the allowed extentions: {}'
            ).format(self.upload_set)
            raise StopValidation(self.message or message)

        if not self.upload_set.file_allowed(field.data, filename):
            raise StopValidation(self.message or
                                 'File does not have an approved extension')

file_allowed = FileAllowed
