@REM -*- coding: windows-1252; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM Purpose:     start des Powerscipt Studios
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
"%CADDOK_RUNTIME%\powerscriptstudio"
