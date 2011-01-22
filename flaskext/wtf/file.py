from flask import request

from wtforms import FileField as _FileField
from wtforms import ValidationError
from wtforms.widgets import FileInput

class FileMultipleInput(FileInput):

    def __call__(self, *args, **kwargs):
        kwargs['multiple'] = u'multiple'
        return super(FileMultipleInput, self).__call__(*args, **kwargs)


class FileField(_FileField):

    @property
    def file(self):
        """
        Returns FileStorage class if available from request.files
        or None
        """
        return request.files.get(self.name, None)


class FileMultipleField(_FileField):
    """
    Supports the HTML5 <input type="file" multiple> spec.

    All files are obtainable from a **files** property.
    """

    widget = FileMultipleInput()

    @property
    def files(self):
        """
        Returns list of files matching name in request.files
        """
        return request.files.getlist(self.name)


class FileRequired(object):

    def __init__(self, message=None):
        self.message=message

    def __call__(self, form, field):
        # support both multiple and single fields
        file = getattr(field, "file", None)
        files = getattr(field, "files", [])

        if not file and not files:
            raise ValidationError, self.message

file_required = FileRequired


class FileAllowed(object):

    def __init__(self, upload_set, message=None):
        self.upload_set = upload_set
        self.message = message

    def __call__(self, form, field):
        # support both multiple and single fields
        file = getattr(field, "file", None)
        files = getattr(field, "files", [])

        if file is not None:
            files.append(file)

        for file in files:
            if not self.upload_set.file_allowed(file, file.filename):

                raise ValidationError, self.message

file_allowed = FileAllowed
    
