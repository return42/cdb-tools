# -*- coding: utf-8; mode: python -*-
u"""misc tools for bootstrapping cdbtools"""
import sys
import re

from fspath import FSPath

BAT_TEMPLATE = u"""@REM -*- coding: windows-1252; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM --                             --  File:     wrapper.bat
REM -- Copyright (C) 2017 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------
REM Purpose:     wrap foo.py to foo.bat
REM ----------------------------------------------------------------------------

IF DEFINED CDBTOOLS_HOME goto cdbtoolsok
for %%%%A IN ("%%~dp0\..\..") DO SET "CDBTOOLS_HOME=%%%%~fA"
IF %%CDBTOOLS_HOME:~-1%%==\ SET CDBTOOLS_HOME=%%CDBTOOLS_HOME:~0,-1%%
call "%%CDBTOOLS_HOME%%\winShortcuts\cdbEnv.bat"
call "%%CDBTOOLS_HOME%%\win_bin\cdbtools-activate.bat"
:cdbtoolsok

REM if NOT EXIST "%%CDBTOOLS_HOME%%\win_bin\ConEmu\ConEmu.exe" goto openCMDNative
REM "%%CDBTOOLS_HOME%%\win_bin\ConEmu\ConEmu.exe" -run "%%CADDOK_RUNTIME%%\python.exe" -m dm.cdbtools.run_ptpython %%*
REM goto Exit

IF EXIST "%%~dpn0.py" (
  "%%CADDOK_RUNTIME%%\%(interpreter)s" "%%~dpn0.py" %%*
  GOTO Exit
)
IF EXIST "%%~dpn0-script.py" (
  "%%CADDOK_RUNTIME%%\%(interpreter)s" "%%~dpn0-script.py" %%*
  GOTO Exit
)

:Exit
"""

PTPYTHON_TEMPLATE = u"""@REM -*- coding: windows-1252; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM --                             --  File:     wrapper.bat
REM -- Copyright (C) 2017 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------
REM Purpose:     wrap ptpython
REM ----------------------------------------------------------------------------

IF DEFINED CDBTOOLS_HOME goto cdbtoolsok
for %%%%A IN ("%%~dp0\..\..") DO SET "CDBTOOLS_HOME=%%%%~fA"
IF %%CDBTOOLS_HOME:~-1%%==\ SET CDBTOOLS_HOME=%%CDBTOOLS_HOME:~0,-1%%
call "%%CDBTOOLS_HOME%%\winShortcuts\cdbEnv.bat"
call "%%CDBTOOLS_HOME%%\win_bin\cdbtools-activate.bat"
:cdbtoolsok

REM if NOT EXIST "%%CDBTOOLS_HOME%%\win_bin\ConEmu\ConEmu.exe" goto openCMDNative
REM "%%CDBTOOLS_HOME%%\win_bin\ConEmu\ConEmu.exe" -run "%%CADDOK_RUNTIME%%\python.exe" -m dm.cdbtools.run_ptpython %%*
REM goto Exit

:openCMDNativ
"%%CADDOK_RUNTIME%%\%(interpreter)s" -m dm.cdbtools.run_ptpython %%*

:Exit
"""

def replace_exe_with_bat(folder, def_py='powerscript.exe', template=BAT_TEMPLATE):
    u"""Legt die *.exe Wrapper mit '!#powerscript' im shebang an.

    Z.B. in ``%CADDOK_TOOLS%/py27/Scripts``
    """
    # pylint: disable=too-many-locals, too-many-branches, too-many-statements

    folder  = FSPath(folder)
    del_map = [
        'activate.bat', 'deactivate.bat'
        , 'python.exe', 'pythonw.exe', 'python27.dll'
        , 'easy_install-2.7.exe.manifest', 'easy_install-2.7.bat', 'easy_install-2.7-script.py'
        , 'pip2.exe'                     , 'pip2.bat'            , 'pip2-script.py'
        , 'pip2.7.exe'                   , 'pip2.7.bat'          , 'pip2.7-script.py'
        , 'ptpython.exe.manifest'        , 'ptpython.exe'
        , 'ptipython.exe.manifest'       , 'ptipython.bat'       , 'ptipython-script.py' , 'ptipython.exe'
        , 'ptpython2.exe.manifest'       , 'ptpython2.bat'       , 'ptpython2-script.py' , 'ptpython2.exe'
        , 'ptipython2.exe.manifest'      , 'ptipython2.bat'      , 'ptipython2-script.py', 'ptipython2.exe'
        , ]
    map_py = {
        'pip'                : ('python.exe', BAT_TEMPLATE)
        , 'pip2'             : ('python.exe', BAT_TEMPLATE)
        , 'pip27'            : ('python.exe', BAT_TEMPLATE)
        , 'wheel'            : ('python.exe', BAT_TEMPLATE)
        , 'easy_install'     : ('python.exe', BAT_TEMPLATE) # ?
        , 'virtualenv'       : ('python.exe', BAT_TEMPLATE)
        , 'which'            : ('python.exe', BAT_TEMPLATE)
        , 'fspath'           : ('python.exe', BAT_TEMPLATE)
        , 'activate_this'    : None
        , 'ptpython'         : {'cdbtools-python'       : ('python.exe',      PTPYTHON_TEMPLATE)
                                , 'cdbtools-powerscript': ('powerscript.exe', PTPYTHON_TEMPLATE)
                                , }
        , }

    def log(msg):
        u"""log to stderr"""
        sys.stderr.write(msg + "\n")

    def _wrap_bat(py_fname, wrapper_name, interpreter, bat_script):
        exe_fname  = wrapper_name + '.exe'
        bat_fname  = wrapper_name + '.bat'
        log("generate: %s" % bat_fname)
        if bat_fname.EXISTS:
            #log("          .bat file exits, try to remove ..")
            bat_fname.rmfile()

        if exe_fname.EXISTS:
            #log("          .exe file exits, try to remove ..")
            exe_fname.rmfile()

        #log("          create shebang & bat-wrapper with interpreter: '%s' " % interpreter)
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

        #log("          prepare python script: '%s' " % py_fname)
        with py_fname.openTextFile(mode="w") as pyf:
            pyf.write(new_script)

        #log("          create bat wrapper: '%s' " % bat_fname)
        with bat_fname.openTextFile(mode="w") as bat:
            bat.write(bat_script)
        # if bat_fname.EXISTS:
        #     log("          %s OK" % bat_fname)
        # else:
        #     log("          %s ERROR" % bat_fname)

    # delete files
    # ------------

    for d in del_map:
        d = folder / d
        if d.EXISTS:
            log("delete: %s" % d)
            d.delete()

    # create bat wrapper
    # ------------------

    for py_fname in folder.glob("*.py"):
        fname = FSPath(re.sub(r'(-script\.pyw?|.pyw?)?$', '', py_fname)).relpath(folder)
        wrappers = map_py.get(fname, (def_py, template))
        if wrappers is None:
            log("skip:     %s" % py_fname)
            continue
        if not isinstance(wrappers, dict):
            wrappers = {fname : wrappers}

        for wrapper_name, (interpreter, template) in wrappers.items():
            bat_script = template % locals()
            _wrap_bat(py_fname, folder/wrapper_name, interpreter, bat_script)
