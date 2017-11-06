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

def replace_exe_with_bat(folder, interpreter=None):
    u"""Legt die *.exe Wrapper mit '!#powerscript' im shebang an.

    Z.B. in ``%CADDOK_TOOLS%/py27/Scripts``
    """
    from fspath.win import wrapScriptExe
    def log(msg):
        sys.stderr.write(msg + "\n")

    folder = FSPath(folder)
    def_py = interpreter or 'powerscript.exe'

    delete = ['python.exe', 'pythonw.exe'
              , 'pip2.bat'   , 'pip2.exe'  , 'pip2-script.py'
              , 'pip2.7.bat' , 'pip2.7.exe', 'pip2.7-script.py'
              , 'activate.bat', 'deactivate.bat'
              , 'ptpython.exe', 'ptpython.exe.manifest'
              , 'ptipython.bat' , 'ptipython.exe'   , 'ptipython.exe.manifest' ,  'ptipython-script.py'
              , 'ptpython2.bat' , 'ptpython2.exe'   , 'ptpython2.exe.manifest' ,  'ptpython2-script.py'
              , 'ptipython2.bat', 'ptipython2.exe'  , 'ptipython2.exe.manifest',  'ptipython2-script.py'
              , ]
    map_py = {'pip'            : 'python.exe'
              , 'pip2'         : 'python.exe'
              , 'pip27'        : 'python.exe'
              , 'wheel'        : 'python.exe'
              , 'easy_install' : 'python.exe' # ?
              , 'virtualenv'   : 'python.exe'
              , 'which'        : 'python.exe'
              , 'fspath'       : 'python.exe'
              , }

    for d in delete:
        d = folder / d
        if d.EXISTS:
            log("delete: %s" % d)
            d.delete()

    for py_fname in folder.glob("*.py"):

        fname = FSPath(re.sub(r'(-script\.pyw?)?$', '', py_fname)).relpath(folder)

        interpreter = map_py.get(fname, def_py)

        bat_fname  = folder / fname + '.bat'
        exe_fname  = folder / fname + '.exe'
        bat_script = bat_template % locals()

        log("generate: %s" % bat_fname)
        if bat_fname.EXISTS:
            log("          .bat file exits, try to remove ..")
            bat_fname.rmfile()

        if exe_fname.EXISTS:
            log("          .exe file exits, try to remove ..")
            exe_fname.rmfile()

        log("          create shebang & bat-wrapper with interpreter: '%s' " % interpreter)
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

        log("          create bat wrapper: '%s' " % bat_fname)
        with bat_fname.openTextFile(mode="w") as bat:
            bat.write(bat_script)
        if bat_fname.EXISTS:
            log("          %s OK" % bat_fname)
        else:
            log("          %s ERROR" % bat_fname)
