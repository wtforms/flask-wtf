"""
Flask-WTF
---------

Simple integration of Flask and WTForms, including CSRF validation.

Links
`````

* `documentation <http://packages.python.org/Flask-WTF>`_
* `development version
  <http://bitbucket.org/danjac/flask-wtf/get/tip.gz#egg=Flask-WTF>`_


"""
from setuptools import setup


setup(
    name='Flask-WTF',
    version='0.1.2',
    url='http://bitbucket.org/danjac/flask-wtf',
    license='BSD',
    author='Dan Jacob',
    author_email='danjac354@gmail.com',
    description='Simple integration of Flask and WTForms',
    long_description=__doc__,
    packages=['flaskext', 'flaskext.recaptcha'],
    namespace_packages=['flaskext'],
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'WTForms'
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
