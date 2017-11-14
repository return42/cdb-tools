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

REM CDBTools
REM --------

SET "CDBTOOLS_ENV=%CDBTOOLS_HOME%"
SET "CDBTOOLS_PY27=%CDBTOOLS_HOME%\py27"
SET "CDBTOOLS_CACHE=%CDBTOOLS_HOME%\.cache"
SET "CDBTOOLS_DIST=%CDBTOOLS_HOME%\dist"
SET "CDBTOOLS_SW_DOWNLOAD=%CDBTOOLS_DIST%\sw-download"
SET "CDBTOOLS_PIP_DOWNLOAD=%CDBTOOLS_DIST%\pip-download"

REM PROMPT
REM ------

IF DEFINED PROMPT GOTO promptInitOK
    SET "PROMPT=$P$G"
:promptInitOK

IF DEFINED _OLD_CDBTOOLS_PROMPT goto SET_NEW_PROMPT
    SET "_OLD_CDBTOOLS_PROMPT=%PROMPT%"
:SET_NEW_PROMPT
SET "PROMPT=[CDBTools]$s$M$P$S$_$$$S"

REM PYTHONHOME
REM ----------

IF DEFINED _OLD_CDBTOOLS_PYTHONHOME GOTO SET_NEW_PYTHONHOME
    SET "_OLD_CDBTOOLS_PYTHONHOME=%PYTHONHOME%"
:SET_NEW_PYTHONHOME
SET PYTHONHOME=

REM PATH
REM ------

IF DEFINED _OLD_CDBTOOLS_PATH GOTO SET_NEW_PATH
    SET "_OLD_CDBTOOLS_PATH=%PATH%"
:SET_NEW_PATH
SET "PATH=%CADDOK_RUNTIME%;%PATH%"
SET "PATH=%CDBTOOLS_PY27%\Scripts;%PATH%"
SET "PATH=%CDBTOOLS_HOME%\win_bin;%PATH%"

REM the user scheme
REM ---------------
REM https://docs.python.org/2/install/index.html#inst-alt-install-user

IF DEFINED PYTHONUSERBASE GOTO pythonUserInitOK
    SET "PYTHONUSERBASE=%APPDATA%\Python"
:pythonUserInitOK

IF DEFINED _OLD_CDBTOOLS_PYTHONUSERBASE GOTO SET_NEW_USERBASE
    SET "_CDBTOOLS_PYTHONUSERBASE=%PYTHONUSERBASE%"
:SET_NEW_USERBASE
SET "PYTHONUSERBASE=%CDBTOOLS_PY27%"

REM pip config
REM ----------

IF DEFINED PIP_CONFIG_FILE GOTO pipConfigInitOK
    SET "PIP_CONFIG_FILE=%APPDATA%\pip\pip.ini"
:pipConfigInitOK

IF DEFINED _OLD_CDBTOOLS_PIP_CONFIG_FILE GOTO SET_PIP_CONFIG_FILE
    SET "_OLD_CDBTOOLS_PIP_CONFIG_FILE=%PIP_CONFIG_FILE%"
:SET_PIP_CONFIG_FILE
SET "PIP_CONFIG_FILE=%CDBTOOLS_HOME%\bootstrap\pip.ini"


REM PYTHONPATH
REM ----------

IF DEFINED _OLD_CDBTOOLS_PYTHONPATH GOTO SET_NEW_PYTHONPATH
    set "_OLD_CDBTOOLS_PYTHONPATH=%PYTHONPATH%"
:SET_NEW_PYTHONPATH
SET "PYTHONPATH=%CDBTOOLS_HOME%\lib;%PYTHONPATH%"

title CDB-Tools shell
echo ------------------------------------------------------------
echo CDB-Tools environment
echo ------------------------------------------------------------
echo.
echo  CADDOK_RUNTIME: %CADDOK_RUNTIME%
echo  CADDOK_BASE:    %CADDOK_BASE%
echo  CDBTOOLS_HOME:  %CDBTOOLS_HOME%
echo  HOME:           %HOME%
echo.

IF [%1]==[] goto Exit
  %ComSpec% %*

:Exit
