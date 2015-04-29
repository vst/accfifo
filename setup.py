"""
This module provides the setup guidelines.
"""
from setuptools import setup
from setuptools import find_packages
import os

## The absolute directory path:
HERE = os.path.abspath(os.path.dirname(__file__))

## The README file contents:
README = open(os.path.join(HERE, "README.md")).read()

## The LICENSE file contents:
LICENSE = open(os.path.join(HERE, "LICENSE")).read()

## Requirements for installation (non at the moment):
REQUIRED_LIBRARIES = []

## Setup now:
setup(
    name="accfifo",
    version="0.1dev",
    description="A FIFO accounting calculator",
    long_description=README,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Libraries",
    ],
    keywords="accounting fifo",
    author="Vehbi Sinan Tunalioglu",
    author_email="vst@vsthost.com",
    url="https://github.com/vst/accfifo",
    license=LICENSE,
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=REQUIRED_LIBRARIES,
    dependency_links=[],
)
