@REM -*- coding: utf-8; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM Purpose:     Start des cdbsvcd Prozess
REM ----------------------------------------------------------------------------

IF NOT DEFINED CDBTOOLS_HOME (
   call "%~d0%~p0cdbEnv.bat"
)

IF NOT EXIST "%CDBTOOLS_HOME%\win_bin\ConEmu\ConEmu.exe" goto openCMD
  IF NOT [%1]==[conemu] (
    START "ConEmu" "%CDBTOOLS_HOME%\win_bin\ConEmu\ConEmu.exe" -reuse -run %0 conemu
    GOTO Exit
  )

REM ----------------------------------------------------------------------------
:openCMD
REM ----------------------------------------------------------------------------

cd /D "%CADDOK_BASE%"

call "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat"
title %~n0 ^(%CADDOK_DEFAULT%^)

echo ============================================================
echo %~n0 ^(%CADDOK_DEFAULT%^) debug mode!!
echo ============================================================
echo.
echo   CDBTOOLS_HOME:  %CDBTOOLS_HOME%
echo.
echo   CADDOK_RUNTIME: %CADDOK_RUNTIME%
echo   CADDOK_BASE:    %CADDOK_BASE%
echo   CADDOK_DEFAULT: %CADDOK_DEFAULT%
echo.
echo ============================================================
@echo on
START "%~n0 CDBTools (%CADDOK_DEFAULT%)" "%CADDOK_RUNTIME%\cdbsvcd.exe" -d -v -db "%CADDOK_DEFAULT%"
@echo off
echo.
echo ============================================================
echo CDBTools debugger listen to breakpoints
echo ============================================================
echo.
echo hit CTRL-C to stop listening
echo.
"%CADDOK_RUNTIME%\python.exe" -c "from dm.cdbtools.debug import client;client(polltime=3)"
pause
