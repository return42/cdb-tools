# -*- coding: utf-8; mode: python -*-

import sys
import re
from fspath import FSPath

bat_template = u"""@REM -*- coding: windows-1252; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM --                             --  File:     wrapper.bat
REM -- Copyright (C) 2017 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------
REM Purpose:     wrap .py to .bat
REM ----------------------------------------------------------------------------

IF NOT DEFINED CDBTOOLS_HOME (
   echo ERROR: !! This command has to be run in a CDB-Tools environment cdbtools !!
   pause
   GOTO Exit
)

IF EXIST "%%~dpn0.py" (
  %(interpreter)s "%%~dpn0.py" %%*
  GOTO Exit
)
IF EXIST "%%~dpn0-script.py" (
  %(interpreter)s "%%~dpn0-script.py" %%*
  GOTO Exit
)

:Exit
"""

def replace_exe_with_bat(folder, interpreter=u"powerscript", ignore=None):
    u"""Legt die *.exe Wrapper mit '!#powerscript' im shebang an.

    Z.B. in ``%CADDOK_TOOLS%/py27/Scripts``
    """
    from fspath.win import wrapScriptExe

    def log(msg):
        sys.stderr.write(msg + "\n")
    if ignore is None:
        ignore = ['easy_install', 'pip', 'wheel']
    folder = FSPath(folder)
    for py_file in folder.glob("*.py"):

        if [i for i in ignore if py_file.BASENAME.startswith(i)]:
            continue

        exe_fname  = FSPath(re.sub(r'(-script\.pyw?|\.exe)?$', '.exe', py_file))
        bat_fname  = FSPath(re.sub(r'(-script\.pyw?|\.exe)?$', '.bat', py_file))
        bat_script = bat_template % locals()

        log("generate: %s" % bat_fname)
        if bat_fname.EXISTS:
            log("          .bat file exits, try to remove ..")
            bat_fname.rmfile()

        if exe_fname.EXISTS:
            log("          .exe file exits, try to remove ..")
            exe_fname.rmfile()

        log("          create wrapper with interpreter: '%s' " % interpreter)
        with bat_fname.openTextFile(mode="w") as bat:
            bat.write(bat_script)
        if bat_fname.EXISTS:
            log("generate: %s OK" % bat_fname)
        else:
            log("generate: %s ERROR" % bat_fname)
