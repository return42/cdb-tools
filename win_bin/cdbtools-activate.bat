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

rem IF NOT DEFINED CADDOK_TOOL (
rem    echo ERROR: script %~n0 missing CADDOK_TOOL environment
rem    goto Exit
rem )

if [%1]==[--] (
  goto SetEnv
) ELSE (
  %ComSpec% /K %0 -- %*
  goto Exit
)

:SetEnv
SET CDBTOOLS_ENV=%CDBTOOLS_HOME%
SET CDBTOOLS_PY27=%CDBTOOLS_HOME%\py27
SET PYTHONPATH=%CDBTOOLS_HOME%\lib;%CDBTOOLS_PY27%\Lib\site-packages;%PYTHONPATH%
SET PATH=%CDBTOOLS_HOME%\win_bin;%CDBTOOLS_PY27%\Scripts;%PATH%

if [%1]==[--] (
  SHIFT /1
)

if NOT '%1' == '' (
  REM FIXME: Workaround, dieses bekloppte SHIFT von M$-Win shiebt
  REM nicht die Argumente in %*
  %1 %2 %3 %4 %5 %6 %7 %8 %9
  GOTO Exit
)

title CDB-Tools shell
SET PROMPT=[CDB-Tools]$s$M$P$S$_$$$S
echo ------------------------------------------------------------
echo CDB-Tools environment
echo ------------------------------------------------------------
echo.
echo  CDBTOOLS_HOME: %CDBTOOLS_HOME%
echo  HOME:          %HOME%
GOTO Exit

REM ----------------------------------------------------------------------------
:Exit
REM ----------------------------------------------------------------------------
