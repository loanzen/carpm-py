#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup


requirements = [
    "requests",
    "pytest"
]

setup(
    name='carpm',
    version='0.1.0',
    description="",
    long_description='',
    author="Kshitij Mittal",
    author_email='kshitij@loanzen.in',
    url='https://github.com/loanzen/carpm-py',
    packages=[
        'carpm',
    ],
    package_dir={'carpm':
                 'carpm'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
)
