"""
Flask-WTF
=========

Simple integration of Flask and WTForms, including CSRF, file upload
and Recaptcha integration.

Links
-----

* `documentation <https://flask-wtf.readthedocs.org>`_
* `development version
  <http://github.com/lepture/flask-wtf>`_


"""
try:
    import multiprocessing
except ImportError:
    pass

import re
from setuptools import setup

with open('flask_wtf/__init__.py') as f:
    m = re.findall(r'__version__\s*=\s*\'(.*)\'', f.read())
    version = m[0]


setup(
    name='Flask-WTF',
    version=version,
    url='http://github.com/lepture/flask-wtf',
    license='BSD',
    author='Dan Jacob',
    author_email='danjac354@gmail.com',
    maintainer='Hsiaoming Yang',
    maintainer_email='me@lepture.com',
    description='Simple integration of Flask and WTForms',
    long_description=__doc__,
    packages=[
        'flask_wtf',
        'flask_wtf.recaptcha'
    ],
    test_suite='nose.collector',
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'Werkzeug>=0.9.5',
        'WTForms>=1.0.5'
    ],
    tests_require=[
        'nose',
        'Flask-Babel',
    ],
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: Implementation',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
