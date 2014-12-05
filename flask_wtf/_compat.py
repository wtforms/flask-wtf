import sys
if sys.version_info[0] == 3:
    text_type = str
    string_types = (str,)
else:
    text_type = unicode
    string_types = (str, unicode)


def to_bytes(text):
    """Transform string to bytes."""
    if isinstance(text, text_type):
        text = text.encode('utf-8')
    return text


def to_unicode(input_bytes, encoding='utf-8'):
    """Decodes input_bytes to text if needed."""
    if not isinstance(input_bytes, string_types):
        input_bytes = input_bytes.decode(encoding)
    return input_bytes
