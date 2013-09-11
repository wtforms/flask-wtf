"""
Flask-WTF
=========

Simple integration of Flask and WTForms, including CSRF, file upload
and Recaptcha integration.

Links
-----

* `documentation <https://flask-wtf.readthedocs.org>`_
* `development version
  <http://github.com/ajford/flask-wtf>`_


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
    url='http://github.com/ajford/flask-wtf',
    license='BSD',
    author='Dan Jacob',
    author_email='danjac354@gmail.com',
    maintainer='Anthony J. Ford',
    maintainer_email='ford.anthonyj@gmail.com',
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
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
