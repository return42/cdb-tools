@REM -*- coding: utf-8; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM Purpose:     Start des cdbedgesvcd.exe Prozess
REM ----------------------------------------------------------------------------

call "%~d0%~p0cdbEnv.bat"

color 0E
title %~n0 ^(%CADDOK_DEFAULT%^)
cd /D "%CADDOK_BASE%"

REM Am Edge-Standort besteht keine DB Verbindung
SET "CADDOK_DBNAME="
SET "CADDOK_DEFAULT="

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
"%CADDOK_RUNTIME%\cdbedgesvcd.exe" --debug --pid -v --instancedir "%CADDOK_BASE%"
@echo off

echo "-- ENDE --"

REM pause
