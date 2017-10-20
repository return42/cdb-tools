@REM -*- coding: windows-1252; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM Purpose:     Start des cdbsvcd Prozess
REM ----------------------------------------------------------------------------

call "%~d0%~p0cdbEnv.bat"
call "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat" --

color 0E
title %~n0 (%CADDOK_DEFAULT%)
cd /D "%CADDOK_BASE%"

echo ============================================================
echo %~n0 (%CADDOK_DEFAULT%) debug mode!!
echo ============================================================
echo.
echo   CADDOK_RUNTIME: %CADDOK_RUNTIME%
echo   CADDOK_BASE:    %CADDOK_BASE%
echo   CADDOK_DEFAULT: %CADDOK_DEFAULT%
echo.
echo ============================================================

@echo on
START "%~n0 (%CADDOK_DEFAULT%)" "%CADDOK_RUNTIME%\cdbsvcd.exe" -d -v -db "%CADDOK_DEFAULT%"
@echo off
echo waiting for remote debug session ...

"%CADDOK_RUNTIME%\python.exe" -c "from fspath.debug import rtrace_client;rtrace_client(polltime=3)"
pause
