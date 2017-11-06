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

set "VIRTUAL_ENV=%CDBTOOLS_HOME%\py27"

if defined _OLD_VIRTUAL_PROMPT (
    set "PROMPT=%_OLD_VIRTUAL_PROMPT%"
) else (
    if not defined PROMPT (
        set "PROMPT=$P$G"
    )
    set "_OLD_VIRTUAL_PROMPT=%PROMPT%"
)
set "PROMPT=(py27) %PROMPT%"

REM Don't use () to avoid problems with them in %PATH%
if defined _OLD_VIRTUAL_PYTHONHOME goto ENDIFVHOME
    set "_OLD_VIRTUAL_PYTHONHOME=%PYTHONHOME%"
:ENDIFVHOME

REM set "PYTHONHOME=%CDBTOOLS_HOME%\py27"
set PYTHONHOME=

if not defined _OLD_VIRTUAL_PATH goto ENDIFVPATH1
    set "PATH=%_OLD_VIRTUAL_PATH%"
:ENDIFVPATH1
if defined _OLD_VIRTUAL_PATH goto ENDIFVPATH2
    set "_OLD_VIRTUAL_PATH=%PATH%"
:ENDIFVPATH2

set "PATH=%VIRTUAL_ENV%\Scripts;%PATH%"

REM CDBTools environment
REM --------------------

:SetCDBToolsEnv
SET "CDBTOOLS_ENV=%CDBTOOLS_HOME%"
SET "CDBTOOLS_PY27=%CDBTOOLS_HOME%\py27"

SET "PATH=%CDBTOOLS_HOME%\win_bin;%CDBTOOLS_PY27%\Scripts;%CADDOK_RUNTIME%;%PATH%"

if not defined _OLD_VIRTUAL_PYTHONPATH goto ENDIFPYTHONPATH1
    set "PATH=%_OLD_VIRTUAL_PYTHONPATH%"
:ENDIFPYTHONPATH1
if defined _OLD_VIRTUAL_PYTHONPATH goto ENDIFPYTHONPATH2
    set "_OLD_VIRTUAL_PYTHONPATH=%PATH%"
:ENDIFPYTHONPATH2

SET "PYTHONPATH=%CDBTOOLS_HOME%\lib;%CDBTOOLS_PY27%\Lib\site-packages;%PYTHONPATH%"

title CDB-Tools shell
SET PROMPT=[CDB-Tools]$s$M$P$S$_$$$S
echo ------------------------------------------------------------
echo CDB-Tools environment
echo ------------------------------------------------------------
echo.
echo  CADDOK_RUNTIME: %CADDOK_RUNTIME%
echo  CADDOK_BASE:    %CADDOK_BASE%
echo  CDBTOOLS_HOME:  %CDBTOOLS_HOME%
echo  HOME:           %HOME%
echo.

if [%1]==[--] %ComSpec%
