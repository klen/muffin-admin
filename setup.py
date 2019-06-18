#!/usr/bin/env python

import re
from os import path as op

from setuptools import setup, find_packages


def _read(fname):
    try:
        return open(op.join(op.dirname(__file__), fname), encoding='utf-8').read().strip()
    except IOError:
        return ''


_meta = _read('muffin_admin/__init__.py')
_license = re.search(r'^__license__\s*=\s*"(.*)"', _meta, re.M).group(1)
_project = re.search(r'^__project__\s*=\s*"(.*)"', _meta, re.M).group(1)
_version = re.search(r'^__version__\s*=\s*"(.*)"', _meta, re.M).group(1)

install_requires = [
    l for l in _read('requirements.txt').split('\n')
    if l and not l.startswith('#')]

setup(
    name=_project,
    version=_version,
    license=_license,
    description=_read('DESCRIPTION'),
    long_description=_read('README.rst'),
    #  long_description_content_type='text/markdown',
    platforms=('Any'),
    keywords = "asyncion aiohttp muffin admin".split(), # noqa

    author='Kirill Klenov',
    author_email='horneds@gmail.com',
    url='https://github.com/klen/muffin-admin',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Natural Language :: English',
        'Natural Language :: Russian',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Testing',
        'Topic :: Utilities',
    ],

    packages=find_packages(),
    include_package_data=True,
    install_requires=install_requires,
)
