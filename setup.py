import os
from setuptools import setup
README = os.path.join(os.path.dirname(__file__), 'README.md')
try:
    import pypandoc
    LONG = pypandoc.convert(README,format='md', to='rst')
except ImportError as e:
    print (e)
    LONG = open(README).read()

setup(
    name="pytimecamp",
    version="0.1.4",
    author="Steven Rossiter",
    author_email="steve@agiletek.co.uk",
    description=("A wrapper around the Timecamp API."),
    license = "MIT",
    url = "https://pythonhosted.org/pytimecamp/",
    packages=['pytimecamp'],
    long_description=LONG,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Win32 (MS Windows)",
        "Programming Language :: Python :: 3.4"
    ],
)
