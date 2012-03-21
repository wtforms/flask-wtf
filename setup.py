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
    version='0.6',
    url='http://github.com/rduplain/flask-wtf',
    license='BSD',
    author='Dan Jacob',
    author_email='danjac354@gmail.com',
    maintainer='Ron DuPlain',
    maintainer_email='ron.duplain@gmail.com',
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
