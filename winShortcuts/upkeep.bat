@REM -*- coding: windows-1252; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM --                             --  File:     maintain.bat
REM -- Copyright (C) 2017 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------
REM Purpose:     script for CDB-Tools maintenance
REM ----------------------------------------------------------------------------

call "%~d0%~p0cdbEnv.bat"

chcp 1252 >NUL

title %~n0 (%CADDOK_DEFAULT%)
REM cd /D %CADDOK_BASE%

echo ============================================================
echo %~n0 (%CADDOK_DEFAULT%)
echo ============================================================
echo.
echo   CADDOK_RUNTIME: %CADDOK_RUNTIME%
echo   CADDOK_BASE:    %CADDOK_BASE%
echo   CADDOK_DEFAULT: %CADDOK_DEFAULT%
echo.
echo ============================================================

IF NOT EXIST %CADDOK_RUNTIME% (
   echo ERROR: missing %CADDOK_RUNTIME%
   echo ERROR: fix your CADDOK_RUNTIME environment in config file::
   echo ERROR:
   echo ERROR:    %CDBTOOLS_HOME%\winShortcuts\cdbEnv
   echo ERROR:
   goto Exit
)

IF NOT EXIST %CDBTOOLS_HOME%\py27\Scripts goto installSTART
CHOICE /C YN /M "Sollen die Software für cdbtools eingerichtet werden?"
IF ERRORLEVEL 2 GOTO installEND
:installSTART
"%CADDOK_RUNTIME%\cdbsh.exe" -c "%CDBTOOLS_HOME%\bootstrap\install.bat"
goto Exit
:installEND

call "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat" >NUL 2>NUL

CHOICE /C YN /M "Sollen Skript-Wrapper aktualisiert werden?"
IF ERRORLEVEL 2 GOTO wrapperEND
call pip-fix-launcher.bat
:wrapperEND

CHOICE /C YN /M "Soll aus den cdbtools ein ZIP gebaut werden?"
IF ERRORLEVEL 2 GOTO zipEND
"%CADDOK_RUNTIME%\python.exe" "%CDBTOOLS_HOME%\bootstrap\build.py" zip-cdbtools
:zipEND

:Exit
pause
