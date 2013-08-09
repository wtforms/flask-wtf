Upgrading to Newer Releases
===========================

Flask-WTF itself is changing like any software is changing over time. Most
of the changes are the nice kind, the kind where you don't have to change
anything in your code to profit from a new release.

However every once in a while there are changes that do require some
changes in your code or there are changes that make it possible for you to
improve your own code quality by taking advantage of new features in
Flask-WTF.

This section of the documentation enumerates all the changes in Flask-WTF
from release to release and how you can change your code to have a painless 
updating experience.

If you want to use the easy_install command to upgrade your Flask-WTF
installation, make sure to pass it the -U parameter::

    $ pip install -U Flask-WTF


Version 0.9.0
-------------

Dropping the imports of wtforms is a big change, it may be lots of pain for
you, but the imports are hard to maintain. Instead of importing ``Fields``
from Flask-WTF, you need to import them from the original wtforms::

    from wtforms import TextField

Configuration name of ``CSRF_ENABLED`` is changed to ``WTF_CSRF_ENABLED``.
There is a chance that you don't need to do anything if you haven't set any
configuration.

This version has many more features, if you don't need them, they will not
break any code of yours.
