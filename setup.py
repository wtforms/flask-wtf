"""
Flask-WTF
---------

Simple integration of Flask and WTForms, including CSRF, file upload
and Recaptcha integration.

Links
`````

* `documentation <http://packages.python.org/Flask-WTF>`_
* `development version
  <http://bitbucket.org/danjac/flask-wtf/get/tip.gz#egg=Flask-WTF>`_


"""
from setuptools import setup


setup(
    name='Flask-WTF',
    version='0.2.3',
    url='http://bitbucket.org/danjac/flask-wtf',
    license='BSD',
    author='Dan Jacob',
    author_email='danjac354@gmail.com',
    description='Simple integration of Flask and WTForms',
    long_description=__doc__,
    packages=['flaskext', 
              'flaskext.wtf', 
              'flaskext.wtf.recaptcha'],
    namespace_packages=['flaskext'],
    test_suite='nose.collector',
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'WTForms'
    ],
    tests_require=[
        'nose',
        'Flask-Testing',
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
