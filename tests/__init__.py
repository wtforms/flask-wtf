# This tests whether __all__ namespace of WTForms is available.
# Fails as AttributeError immediately if an import is missing in flaskext.wtf.
from flaskext.wtf import *

