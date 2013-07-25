import sys
if sys.version_info[0] == 3:
    string_types = (str,)
    string_type = str
else:
    string_type = unicode
    string_types = (str, unicode)


def to_bytes(text):
    """Transform string to bytes."""
    if isinstance(text, string_type):
        text = text.encode('utf-8')
    return text
