#!/usr/bin/env python

import os
import sys
import distutils
from distutils.core import setup
from subprocess import Popen

_top_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_top_dir, 'lib'))
try:
    import wecomp
finally:
    del sys.path[0]

classifiers = '''\
Development Status :: 4 - Beta
Environment :: Console
Intended Audience :: Developers
Intended Audience :: System Administrators
License :: OSI Approved :: GNU General Public License (GPL)
Operating System :: Unix
Topic :: Software Development :: Build Tools
Topic :: Software Development :: Code Generators
Topic :: Software Development :: Compilers
Topic :: Text Processing :: Markup :: HTML
Topic :: Utilities
'''
long_description = '''\
Pack and compress client-side source code.

Features:
 * CSS, JS -- minification and merging files
 * HTML -- minification with proper handling of script and style tags
 * PHP -- same as HTML, but PHP code is left untouched
'''


if sys.version < '2.2.3':
    from distutils.dist import DistributionMetadata
    DistributionMetadata.classifiers = None
    DistributionMetadata.download_url = None

setup(
    name='wecomp',
    version=wecomp.__version__,
    maintainer='Pawel Olejniczak',
    maintainer_email='pawel.olejniczak@gmail.com',
    author='Pawel Olejniczak',
    author_email='pawel.olejniczak@gmail.com',
    url='https://github.com/Eyjafjallajokull/wecomp',
    license='GPL',
    platforms=['linux'],
    package_dir={'': 'lib'},
    py_modules=['wecomp'],
    scripts=['wecomp'],
    description='Pack and compress client-side source code.',
    classifiers=filter(None, classifiers.split('\n')),
    long_description=long_description,
)
