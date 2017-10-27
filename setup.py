#!/usr/bin/python3

from setuptools import setup
import os
import sys
import texas

long_description = read('docs/README.txt')

class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True

    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)

setup(
    name='texas',
    version=texas.__version__,
    url='https://github.com/jsnider-mtu/texas/',
    license='GNU GPL2.0',
    author='Joshua Snider',
    tests_require=['pytest'],
    install_requires=[],
    cmdclass={'test': PyTest},
    author_email='afsa@tinyhippo.ninja',
    description='Texas Hold\'Em as a Service',
    long_description=long_description,
    packages=['texas'],
    include_package_data=True,
    platforms='any',
    test_suite='texas.test.test_texas',
    classifiers = [
        'Programming Language :: Python',
        'Development Status :: 0 - Alpha',
        'Natural Language :: English',
        'Environment :: Web Environment',
        'Intended Audience :: People',
        'License :: GNU GPL2.0',
        'Operating System :: OS Independent',
        'Topic :: Games :: Texas Hold\'Em Poker'
        ],
    extras_require={
        'testing': ['pytest']
    }
)
