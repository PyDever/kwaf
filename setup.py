#!/usr/bin/env python2
# -*- coding: utf-8 -*-

from setuptools import setup

# private meta data globals for modularity
__version__         = '0.1'
__description__     = 'simple WAF security tester and bypasser'
__author__          = 'Kaleb R. Horvath'
__author_email__    = 'bobafett2021@hotmail.com'
__license__         = 'BSD 3-Clause License'

# call Python 2.7.15 setup function from setuptools
setup(
      name='kwaf', version=__version__, description=__description__,
      author=__author__, license=__license__, author_email=__author_email__,
      url='https://github.com/PyDever/kwaf', packages=['kwaf', 'tests'])

# no need for install_requires field, android-install.sh calls requirements.txt
