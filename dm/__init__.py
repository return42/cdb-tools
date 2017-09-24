# -*- coding: utf-8; mode: python -*-

import sys, os
from . import __pkginfo__

# Aktivierung der Python Pakete in den git submodulen
sys.path.append(os.path.join(os.path.dirname(__file__), "fspath"))

__version__   = __pkginfo__.version
__author__    = __pkginfo__.authors[0]
__license__   = __pkginfo__.license
__copyright__ = __pkginfo__.copyright
