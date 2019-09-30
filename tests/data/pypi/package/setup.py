import os
from setuptools import setup

version = open('Ctl/VERSION').read().strip()

# The directory containing this file
HERE = os.path.dirname(__file__)

# The text of the README file
with open(os.path.join(HERE, "README.md")) as fh:
    README = fh.read()

# This call to setup() does all the work
setup(
    name="ctl_pypi_test",
    version=version,
    description="Dummy python package used for testing PyPI releases",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://github.com/20c/ctl_pypi_test",
    author="20c",
    author_email="code@20c.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["ctl_pypi_test"],
    include_package_data=True,
)
