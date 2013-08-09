Installation
============

This part of the documentation covers the installation of Flask-WTF.
The first step to using any software package is getting it properly installed.


Distribute & Pip
----------------

Installing Flask-WTF is simple with `pip <http://www.pip-installer.org/>`_::

    $ pip install Flask-WTF

or, with `easy_install <http://pypi.python.org/pypi/setuptools>`_::

    $ easy_install Flask-WTF

But, you really `shouldn't do that <http://www.pip-installer.org/en/latest/other-tools.html#pip-compared-to-easy-install>`_.



Cheeseshop Mirror
-----------------

If the Cheeseshop is down, you can also install Flask-WTF from one of the
mirrors. `Crate.io <http://crate.io>`_ is one of them::

    $ pip install -i http://simple.crate.io/ Flask-WTF


Get the Code
------------

Flask-WTF is actively developed on GitHub, where the code is
`always available <https://github.com/ajford/flask-wtf>`_.

You can either clone the public repository::

    git clone git://github.com/ajford/flask-wtf.git

Download the `tarball <https://github.com/ajford/flask-wtf/tarball/master>`_::

    $ curl -OL https://github.com/ajford/flask-wtf/tarball/master

Or, download the `zipball <https://github.com/ajford/flask-wtf/zipball/master>`_::

    $ curl -OL https://github.com/ajford/flask-wtf/zipball/master


Once you have a copy of the source, you can embed it in your Python package,
or install it into your site-packages easily::

    $ python setup.py install
