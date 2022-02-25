@REM -*- coding: utf-8; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM Purpose:     Start des cdbsvcd Prozess
REM ----------------------------------------------------------------------------

call "%~d0%~p0cdbEnv.bat"

color 0E
title %~n0 ^(%CADDOK_DEFAULT%^)
cd /D "%CADDOK_BASE%"

echo ============================================================
echo %~n0 ^(%CADDOK_DEFAULT%^)
echo ============================================================
echo.
echo   CADDOK_RUNTIME: %CADDOK_RUNTIME%
echo   CADDOK_BASE:    %CADDOK_BASE%
echo   CADDOK_DEFAULT: %CADDOK_DEFAULT%
echo.
echo ============================================================


echo on

"%CADDOK_RUNTIME%\cdbsvcd.exe" -d -v -db "%CADDOK_DEFAULT%"

@echo off

echo "-- ENDE --"

pause
