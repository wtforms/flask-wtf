import warnings


def to_bytes(text):
    """Transform string to bytes."""
    if isinstance(text, str):
        text = text.encode('utf-8')
    return text


def to_unicode(input_bytes, encoding='utf-8'):
    """Decodes input_bytes to text if needed."""
    if not isinstance(input_bytes, str):
        input_bytes = input_bytes.decode(encoding)
    return input_bytes


class FlaskWTFDeprecationWarning(DeprecationWarning):
    pass


warnings.simplefilter('always', FlaskWTFDeprecationWarning)
warnings.filterwarnings(
    'ignore', category=FlaskWTFDeprecationWarning, module='wtforms|flask_wtf'
)
