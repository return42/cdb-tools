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

def replace_exe_with_bat(folder, interpreter=u"powerscript.exe", ignore=None):
    u"""Legt die *.exe Wrapper mit '!#powerscript' im shebang an.

    Z.B. in ``%CADDOK_TOOLS%/py27/Scripts``
    """
    from fspath.win import wrapScriptExe

    def log(msg):
        sys.stderr.write(msg + "\n")
    if ignore is None:
        ignore = ['easy_install', 'pip', 'wheel']
    folder = FSPath(folder)
    for py_fname in folder.glob("*.py"):

        if [i for i in ignore if py_fname.BASENAME.startswith(i)]:
            continue

        exe_fname  = FSPath(re.sub(r'(-script\.pyw?|\.exe)?$', '.exe', py_fname))
        bat_fname  = FSPath(re.sub(r'(-script\.pyw?|\.exe)?$', '.bat', py_fname))
        bat_script = bat_template % locals()

        log("generate: %s" % bat_fname)
        if bat_fname.EXISTS:
            log("          .bat file exits, try to remove ..")
            bat_fname.rmfile()

        if exe_fname.EXISTS:
            log("          .exe file exits, try to remove ..")
            exe_fname.rmfile()

        log("          create wrapper with interpreter: '%s' " % interpreter)
        py_script = py_fname.readFile().splitlines()
        new_line  = u"import dm.cdbtools # automatic inserted by cdbtools. This will reorder sys.path !!!"
        if [l for l in py_script if l.startswith("import dm.cdbtools")]:
            new_line = u""

        new_script = u""
        start_insert = False
        for l in py_script:
            if l.startswith(u"#!"):
                l = u"#!%s" % interpreter
            if not l.strip().startswith(u"#"):
                start_insert = True
            if new_line and start_insert:
                new_script += new_line + u'\n'
                new_line = ""
            new_script += l + u'\n'

        log("          prepare python script: '%s' " % py_fname)
        with py_fname.openTextFile(mode="w") as py:
            py.write(new_script)

        with bat_fname.openTextFile(mode="w") as bat:
            bat.write(bat_script)
        if bat_fname.EXISTS:
            log("generate: %s OK" % bat_fname)
        else:
            log("generate: %s ERROR" % bat_fname)
