# This tests whether __all__ namespace of WTForms is available.
# Fails as AttributeError immediately if an import is missing in flask.ext.wtf.
from flask.ext.wtf import *

