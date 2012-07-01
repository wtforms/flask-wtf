"""
Flask-WTF
---------

Simple integration of Flask and WTForms, including CSRF, file upload
and Recaptcha integration.

Links
`````

* `documentation <http://packages.python.org/Flask-WTF>`_
* `development version
  <http://github.com/rduplain/flask-wtf>`_


"""
from setuptools import setup


setup(
    name='Flask-WTF',
    version='0.8',
    url='http://github.com/rduplain/flask-wtf',
    license='BSD',
    author='Dan Jacob',
    author_email='danjac354@gmail.com',
    maintainer='Ron DuPlain',
    maintainer_email='ron.duplain@gmail.com',
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
        'WTForms>=1.0'
    ],
    tests_require=[
        'nose',
        'Flask-Testing',
        'Flask-Uploads',
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
