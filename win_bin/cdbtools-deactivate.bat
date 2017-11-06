@REM -*- coding: windows-1252; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM --                             --  File:     cdbtools-activate.bat
REM -- Copyright (C) 2017 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------

IF NOT DEFINED CDBTOOLS_HOME (
   echo ERROR: script %~n0 missing CDBTOOLS_HOME environment
   goto Exit
)

REM python virtualenv
REM -----------------

set VIRTUAL_ENV=

REM Don't use () to avoid problems with them in %PATH%
if not defined _OLD_VIRTUAL_PROMPT goto ENDIFVPROMPT
    set "PROMPT=%_OLD_VIRTUAL_PROMPT%"
    set _OLD_VIRTUAL_PROMPT=
:ENDIFVPROMPT

if not defined _OLD_VIRTUAL_PYTHONHOME goto ENDIFVHOME
    set "PYTHONHOME=%_OLD_VIRTUAL_PYTHONHOME%"
    set _OLD_VIRTUAL_PYTHONHOME=
:ENDIFVHOME

if not defined _OLD_VIRTUAL_PATH goto ENDIFVPATH
    set "PATH=%_OLD_VIRTUAL_PATH%"
    set _OLD_VIRTUAL_PATH=
:ENDIFVPATH


REM python virtualenv
REM -----------------

:SetEnv
SET CDBTOOLS_ENV=
SET CDBTOOLS_PY27=

if not defined _OLD_VIRTUAL_PYTHONPATH goto ENDIFPYTHONPATH
    set "PATH=%_OLD_VIRTUAL_PYTHONPATH%"
    set _OLD_VIRTUAL_PYTHONPATH=
:ENDIFPYTHONPATH
