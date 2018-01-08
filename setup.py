import os
from setuptools import setup

import pytimecamp

setup(
    name="pytimecamp",
    version=pytimecamp.__version__,
    author=pytimecamp.__author__,
    author_email="london@agiletek.co.uk",
    description=("A wrapper around the Timecamp API."),
    license="MIT",
    url="https://pythonhosted.org/pytimecamp/",
    packages=['pytimecamp'],
    install_requires=["requests", "python-dateutil"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Programming Language :: Python :: 3.6"
    ],
)
