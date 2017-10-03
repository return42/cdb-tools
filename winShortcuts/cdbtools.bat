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

"%CADDOK_RUNTIME%\cdbsh.exe" -v -db %CDB_INSTANCE% -c %CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat %*

