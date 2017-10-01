@REM -*- coding: windows-1252; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM --                             --  File:     cdbtools.bat
REM -- Copyright (C) 2017 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------
REM Purpose:     wrap libraries from CDB-Tools
REM ----------------------------------------------------------------------------

IF NOT DEFINED CDBTOOLS_HOME (
   call %~d0%~p0cdbEnv.bat
)

SET PY27=%CDBTOOLS_HOME%\py27

REM wrap environment of the CDB-Tools
SET PYTHONPATH=%CDBTOOLS_HOME%\lib;%CDBTOOLS_HOME%\lib\fspath;%CDBTOOLS_HOME%\py27\Lib\site-packages;%PYTHONPATH%
SET PATH=%CDBTOOLS_HOME%\win_bin;%CDBTOOLS_HOME%\py27\Scripts;%PATH%


REM ----------------------------------------------------------------------------
REM action
REM ----------------------------------------------------------------------------

if '%1' == '' (
  GOTO openCMD
)

IF NOT DEFINED CADDOK_TOOL (
  "%CADDOK_RUNTIME%\cdbsh.exe" -v -db %CDB_INSTANCE% -c %*
) ELSE (
  %ComSpec% /C %*
)

GOTO Exit

REM ----------------------------------------------------------------------------
:openCMD
REM ----------------------------------------------------------------------------

title CDB-Tools shell
SET PROMPT=[CDB-Tools]$s$M$P$S$_$$$S

echo ------------------------------------------------------------
echo CDB-Tools environment
echo ------------------------------------------------------------
echo.
echo  CDBTOOLS_HOME: %CDBTOOLS_HOME%
echo  HOME:          %HOME%
echo.

IF NOT DEFINED CADDOK_TOOL (
  "%CADDOK_RUNTIME%\cdbsh.exe" -v -db %CDB_INSTANCE% -c %ComSpec%
) ELSE (
  %ComSpec%
)

REM ----------------------------------------------------------------------------
:Exit
REM ----------------------------------------------------------------------------
