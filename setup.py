#!/usr/bin/env python
from setuptools import setup, find_packages

with open('README.rst') as f:
    readme = f.read()

setup(
    name='Flask-WTF',
    version='0.13.1',
    url='https://github.com/lepture/flask-wtf',
    license='BSD',
    author='Dan Jacob',
    author_email='danjac354@gmail.com',
    maintainer='Hsiaoming Yang',
    maintainer_email='me@lepture.com',
    description='Simple integration of Flask and WTForms.',
    long_description=readme,
    packages=find_packages(exclude=('tests',)),
    test_suite='nose.collector',
    zip_safe=False,
    platforms='any',
    install_requires=[
        'Flask',
        'Werkzeug',
        'WTForms',
    ],
    tests_require=[
        'nose',
        'Flask-Babel',
    ],
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Framework :: Flask',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: Implementation :: CPython',
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Dynamic Content',
        'Topic :: Software Development :: Libraries :: Python Modules'
    ]
)
