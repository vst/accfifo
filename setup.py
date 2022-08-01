"""
This module provides the setup guidelines.
"""
import os
from distutils.core import setup

## Setup now:
setup(
    name="accfifo",
    version="0.1.2",
    description="A FIFO accounting calculator",
    long_description=open(
        os.path.join(os.path.abspath(os.path.dirname(__file__)), "README.rst")
    ).read(),
    long_description_content_type="text/x-rst",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "License :: OSI Approved :: BSD License",
        "Topic :: Software Development :: Libraries",
    ],
    keywords=["accounting", "fifo"],
    author="Vehbi Sinan Tunalioglu",
    author_email="vst@vsthost.com",
    url="https://github.com/vst/accfifo",
    packages=["accfifo"],
)
