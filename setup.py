from setuptools import setup

setup(
    name="Flask-WTF",
    install_requires=["Flask", "WTForms", "itsdangerous"],
    extras_require={"email": ["email-validator"]},
)
