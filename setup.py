#!/usr/bin/env python
'''
Installer script for whatbetter.
'''

from setuptools import setup
from _constants import __version__

setup(
    name = "xanaxbetter",
    description = "Automatically transcode and upload FLACs on Xanax.Rip.",
    author = 'Zach Denton',
    author_email = 'zacharydenton@gmail.com',
    version = __version__,
    url = 'http://github.com/zacharydenton/whatbetter',
    py_modules = [
        '_constants',
        'tagging',
        'transcode',
        'xanaxapi'
    ],
    scripts = ['xanaxbetter'],
    install_requires = [
        'mutagen',
        'mechanize',
        'requests'
    ]
)
