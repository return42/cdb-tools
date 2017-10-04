@REM -*- coding: windows-1252; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM --                             --  File:     pylint.bat
REM -- Copyright (C) 2017 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------
REM Purpose:     wrap libraries from CDB-Tools
REM ----------------------------------------------------------------------------

IF NOT DEFINED CDBTOOLS_HOME (
   call %~d0%~p0cdbEnv.bat
)

SET RCFILE=

if EXIST %CDBTOOLS_HOME%\templates\pylintrc (
   SET RCFILE=--rcfile=%CDBTOOLS_HOME%\templates\pylintrc
)

if EXIST %CADDOK_BASE%\etc\pylintrc (
   SET RCFILE=--rcfile=%CADDOK_BASE%\etc\pylintrc
)

call %CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat --

"%CADDOK_RUNTIME%\powerscript.exe" -db %CDB_INSTANCE% %CDBTOOLS_HOME%\py27\Scripts\pylint-script.py %RCFILE% %*
