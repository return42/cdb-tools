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
echo %~n0 CDB-Tools
echo ============================================================
echo.
echo   CDBTOOLS_HOME:  %CDBTOOLS_HOME%
echo   CADDOK_RUNTIME: %CADDOK_RUNTIME%
echo   CADDOK_BASE:    %CADDOK_BASE%
echo   CADDOK_DEFAULT: %CADDOK_DEFAULT%
echo.
echo ============================================================

IF NOT EXIST "%CADDOK_RUNTIME%" (
   echo WARNING: missing CADDOK_RUNTIME at "%CADDOK_RUNTIME%"
   pause
)

IF NOT EXIST "%CADDOK_BASE%" (
   echo WARNING: missing CADDOK_BASE at "%CADDOK_BASE%"
   pause
)

SET "PATH=%CADDOK_RUNTIME%;%PATH%"

REM check python available
WHERE python.exe >NUL  2>NUL
IF %ERRORLEVEL% EQU 0 goto pythonOK
echo ERROR: Python 2.7.9 is needed !!!
goto Exit

:pythonOK

ECHO.
ECHO ===============
ECHO bootstrap
ECHO ===============
ECHO.

IF NOT EXIST "%CDBTOOLS_HOME%\py27\Python27" GOTO bootstrap
CHOICE /C YN /M "Soll ein *Bootstap* durchgeführt werden"
IF ERRORLEVEL 2 GOTO bootstrapOK

:bootstrap
    START /B /WAIT "bootstrap" "%CDBTOOLS_HOME%\bootstrap\bootstrap.bat"
    IF NOT %ERRORLEVEL% EQU 0 GOTO Exit
    CALL "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat" >NUL 2>NUL
    GOTO download

:bootstrapOK
    ECHO bootstrap OK
    call "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat" >NUL 2>NUL

ECHO.
ECHO ===============
ECHO download
ECHO ===============
ECHO.

CHOICE /C YN /M "Sollen die Software Pakete der CDBTools runtergeladen werden (download)"
IF ERRORLEVEL 2 GOTO downloadOK

:download
    CALL "%CDBTOOLS_HOME%\bootstrap\download-all.bat"

:downloadOK

ECHO.
ECHO ===============
ECHO install
ECHO ===============
ECHO.

CHOICE /C YN /M "Sollen die runtergeladenen Software Pakete eingerichtet werden"
IF ERRORLEVEL 2 GOTO installOK

:install
    CALL "%CDBTOOLS_HOME%\bootstrap\install-all.bat"
    CALL "%CDBTOOLS_HOME%\win_bin\cdbtools-fix-launcher.bat"
    GOTO launcherOK

:installOK

ECHO.
ECHO ===============
ECHO update launcher
ECHO ===============
ECHO.

CHOICE /C YN /M "Sollen Launcher der Python Skripte aktualisiert werden"
IF ERRORLEVEL 2 GOTO launcherOK

:launcher
    CALL "%CDBTOOLS_HOME%\win_bin\cdbtools-fix-launcher.bat"

:launcherOK


ECHO.
ECHO ===============
ECHO ZIP CDB-Tools
ECHO ===============
ECHO.

CHOICE /C YN /M "Soll aus den cdbtools ein ZIP gebaut werden"
IF ERRORLEVEL 2 GOTO zipOK

:zip
    python.exe "%CDBTOOLS_HOME%\bootstrap\build.py" dist
:zipOK


:Exit
pause
exit 0

