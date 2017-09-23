@REM -*- coding: windows-1252; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM --                             --  File:     cdbSHELL.bat
REM -- Copyright (C) 2017 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------
REM Purpose:     start CDB shell prompt
REM ----------------------------------------------------------------------------

call %~d0%~p0cdbEnv.bat

title %~n0 (%CDB_INSTANCE%)
cd /D %CADDOK_BASE%

echo ============================================================
echo %~n0 (%CDB_INSTANCE%)
echo ============================================================
echo.
echo   CADDOK_RUNTIME: %CADDOK_RUNTIME%
echo   CADDOK_BASE:    %CADDOK_BASE%
echo   Instanz:        %CDB_INSTANCE%
echo.
echo ============================================================

@echo on
"%CADDOK_RUNTIME%\cdbsh.exe" -v -db %CDB_INSTANCE%
