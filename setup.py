import os
from setuptools import setup

setup(
    name="pytimecamp",
    version="0.1.6",
    author="Steven Rossiter",
    author_email="steve@agiletek.co.uk",
    description=("A wrapper around the Timecamp API."),
    license = "MIT",
    url = "https://pythonhosted.org/pytimecamp/",
    packages=['pytimecamp'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Win32 (MS Windows)",
        "Programming Language :: Python :: 3.4"
    ],
)
