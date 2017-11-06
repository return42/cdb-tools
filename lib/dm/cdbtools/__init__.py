# -*- coding: utf-8; mode: python -*-

# -------------
# sort sys.path
# -------------
#
# .. hint::
#
#    While importing cdbtools, the RTE is manipulated: all pathes with
#    $CDBTOOLS_HOME are placed in front of sys.path
#
#    Reordering sys.path has to be the first task!!
#

import sys, os
if os.environ.get("CDBTOOLS_HOME", None) is None:
    raise Exception("Missing CDBTOOLS_HOME environment, can't init cdbtools!")
sys.path = sorted(sys.path, key=lambda x: x.startswith(os.environ.get("CDBTOOLS_HOME", None)), reverse=True)

# shortcuts

from dm.cdbtools.debug import breakpoint as BP

import ptpython
