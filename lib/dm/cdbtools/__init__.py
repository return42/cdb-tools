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

OLD_SYS_PATH = sys.path[:]
OLD_ENV_PATH = os.environ.get("PATH", None)

if os.environ.get("CDBTOOLS_HOME", None) is None:
    raise Exception("Missing CDBTOOLS_HOME environment, can't init cdbtools!")

# this is just a previos sort for the following imports
sys.path = sorted(sys.path, key=lambda x: x.startswith(os.environ.get("CDBTOOLS_HOME", None)), reverse=True)
# now we can start our imports
from fspath import FSPath, OS_ENV
import platform

# CDBTools environment
# -------------------

CDBTOOLS_HOME         = FSPath(OS_ENV.CDBTOOLS_HOME).ABSPATH
CDBTOOLS_PY27         = FSPath(OS_ENV.CDBTOOLS_PY27).ABSPATH
CDBTOOLS_CACHE        = FSPath(OS_ENV.CDBTOOLS_CACHE).ABSPATH
CDBTOOLS_DIST         = FSPath(OS_ENV.CDBTOOLS_DIST).ABSPATH
CDBTOOLS_SW_DOWNLOAD  = FSPath(OS_ENV.CDBTOOLS_SW_DOWNLOAD).ABSPATH
CDBTOOLS_PIP_DOWNLOAD = FSPath(OS_ENV.CDBTOOLS_PIP_DOWNLOAD).ABSPATH

# sys.path
# --------

CDBTOOLS_SYS_PATH = ['', str(CDBTOOLS_HOME/'lib'), ]
for p in sys.path:
    if (FSPath(p).ABSPATH.startswith(CDBTOOLS_HOME)
        and p not in CDBTOOLS_SYS_PATH):
        CDBTOOLS_SYS_PATH.append(p)

for p in sys.path:
    if (not FSPath(p).ABSPATH.startswith(CDBTOOLS_HOME)
        and p not in CDBTOOLS_SYS_PATH):
        CDBTOOLS_SYS_PATH.append(p)

# in-place repalcement, do not create new object!
sys.path[:] = CDBTOOLS_SYS_PATH

# python setup
# ------------

PIP_REQUIEMENTS = CDBTOOLS_HOME/'bootstrap'/'requirements.txt'

# environment
# -----------

OS_ENV.PYTHONUSERBASE  = str(CDBTOOLS_PY27)
OS_ENV.PIP_CONFIG_FILE = str(CDBTOOLS_HOME/'bootstrap'/'pip.ini')

NEW_ENV_PATH = [CDBTOOLS_PY27/'bin', ]
if platform.system() == 'Windows':
    NEW_ENV_PATH = [str(CDBTOOLS_HOME/'win_bin'), str(CDBTOOLS_PY27/'Scripts'), ]

for p in OS_ENV.PATH.split(os.pathsep):
    if p not in NEW_ENV_PATH:
        NEW_ENV_PATH.append(p)

OS_ENV.PATH = os.pathsep.join(NEW_ENV_PATH)


# prompt
# ------
# FIXME: will not be used in ptpython

sys.ps1 = "CDBTools >>> "
sys.ps2 = "         ... "

# shortcuts

from dm.cdbtools.debug import breakpoint as BP


