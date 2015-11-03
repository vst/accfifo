"""
This module provides the setup guidelines.
"""
from distutils.core import setup

## Setup now:
setup(
    name="accfifo",
    version="0.1.2dev",
    description="A FIFO accounting calculator",
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
