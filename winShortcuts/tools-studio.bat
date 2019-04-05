@REM -*- coding: windows-1252; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM Purpose:     start des Powerscipt Studios
REM ----------------------------------------------------------------------------

call "%~d0%~p0cdbEnv.bat"

title %~n0 ^(%CADDOK_DEFAULT%^)
cd /D %CADDOK_BASE%

echo ============================================================
echo %~n0 ^(%CADDOK_DEFAULT%^)
echo ============================================================
echo.
echo   CADDOK_RUNTIME: %CADDOK_RUNTIME%
echo   CADDOK_BASE:    %CADDOK_BASE%
echo   CADDOK_DEFAULT: %CADDOK_DEFAULT%
echo.
echo ============================================================

call "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat"
@echo on
"%CADDOK_RUNTIME%\powerscriptstudio"
