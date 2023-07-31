#!/usr/bin/python3

import os
import sys
from setuptools import setup

import poker

with open("docs/README.txt", "r") as f:
    long_description = f.read()

# class PyTest(TestCommand):
#    def finalize_options(self):
#        TestCommand.finalize_options(self)
#        self.test_args = []
#        self.test_suite = True
#
#    def run_tests(self):
#        import pytest
#        errcode = pytest.main(self.test_args)
#        sys.exit(errcode)

setup(
    name="poker",
    version=poker.__version__,
    url="https://github.com/jsnider-mtu/poker/",
    license="GNU GPL2.0",
    author="Joshua Snider",
    # tests_require=['pytest'],
    install_requires=[],
    # cmdclass={'test': PyTest},
    author_email="afsa@tinyhippo.ninja",
    description="Poker module for creating games",
    long_description=long_description,
    packages=["poker"],
    include_package_data=True,
    platforms="any",
    # test_suite='poker.test.test_poker',
    classifiers=[
        "Programming Language :: Python",
        "Development Status :: 0 - Alpha",
        "Natural Language :: English",
        "Environment :: Web Environment",
        "Intended Audience :: People",
        "License :: GNU GPL2.0",
        "Operating System :: OS Independent",
        "Topic :: Games :: Poker",
    ],
    # extras_require={
    #    'testing': ['pytest']
    # }
)
