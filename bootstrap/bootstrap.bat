@REM -*- coding: utf-8; mode: bat -*-
@ECHO off
REM ----------------------------------------------------------------------------
REM --                             --  File:     cdbtools.bat
REM -- Copyright (C) 2022 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------
REM Purpose:     bootstrap CDBTools
REM ----------------------------------------------------------------------------

SET PIP_CMD=pip2.exe
SET PYTHON_CMD=python.exe

FOR %%A IN ("%~dp0\..") DO SET "CDBTOOLS_HOME=%%~fA"
IF %CDBTOOLS_HOME:~-1%==\ SET CDBTOOLS_HOME=%CDBTOOLS_HOME:~0,-1%

SET "CDBTOOLS_ENV=%CDBTOOLS_HOME%"
SET "CDBTOOLS_PY27=%CDBTOOLS_HOME%\py27"
SET "CDBTOOLS_CACHE=%CDBTOOLS_HOME%\.cache"
SET "CDBTOOLS_DIST=%CDBTOOLS_HOME%\dist"
SET "CDBTOOLS_SW_DOWNLOAD=%CDBTOOLS_DIST%\sw-download"

IF NOT EXIST "%CDBTOOLS_PY27%" goto CDBTOOLS_PY27_removed
echo ERROR: To bootstrap, first remove (or rename) folder:
echo ERROR:
echo ERROR:   %CDBTOOLS_PY27%
echo.
exit 42
:CDBTOOLS_PY27_removed

IF EXIST "%CDBTOOLS_HOME%\subs\fspath\setup.py" GOTO foundSubs
echo ERROR: missing %CDBTOOLS_HOME%\subs\fspath\setup.py
echo ERROR: forgot to clone with --recursive option?
echo ERROR: before bootstrap first run::
echo ERROR:
echo ERROR:    git submodule init
echo ERROR:    git submodule update
echo.
exit 42
:foundSubs

IF NOT [%PIP_PY_PLATFORM%]==[] GOTO PIP_PY_PLATFORM_OK
echo ERROR: missing environment PIP_PY_PLATFORM in cdbEnv
echo.
exit 42
:PIP_PY_PLATFORM_OK


IF EXIST "%CADDOK_RUNTIME%" (
  echo using CDB's python from: %CADDOK_RUNTIME%\python.exe
  goto :main
)

SET _MISSING_CDB=Y
echo INFO: bootstrap without CDB installation available

REM ----------------------------------------------------------------------------
REM If CDB is not available, we have to use an alternative python 2.7 version to
REM bootstrap (download devTools packages).
REM ----------------------------------------------------------------------------
REM ---- START
REM ----------------------------------------------------------------------------

WHERE %PYTHON_CMD% >NUL  2>NUL
IF %ERRORLEVEL% EQU 0 GOTO pythonExists
echo ERROR: no %PYTHON_CMD% available / Python 2.7.9 is needed !!!
exit 42
:pythonExists

WHERE %PIP_CMD% >NUL  2>NUL
IF %ERRORLEVEL% EQU 0 GOTO pipExists
echo ERROR: no %PIP_CMD% available
exit 42
:pipExists

FOR /f %%i IN ('WHERE %PYTHON_CMD%') DO SET "MYPYTHON_EXE=%%i"
echo found: %MYPYTHON_EXE%
echo.
"%MYPYTHON_EXE%" --version
CHOICE /C YN /M "continue with this version (a python 2.7 is needed!)"
IF %ERRORLEVEL% EQU 1 goto pythonOK
echo ERROR: ^at least a Python 2.7.9 installation is needed !!!
echo ERROR: If you do not have CDB vailable ^(CADDOK_RUNTIME^)
echo ERROR: first install python 2.7 from https://www.python.org/downloads/
exit 42
:pythonOK

REM ----------------------------------------------------------------------------
REM ---- END
REM ----------------------------------------------------------------------------

:main

REM create needed folders
REM ---------------------

MD "%CDBTOOLS_PY27%"            >NUL 2>NUL
MD "%CDBTOOLS_CACHE%"           >NUL 2>NUL
MD "%CDBTOOLS_DIST%"            >NUL 2>NUL
MD "%CDBTOOLS_SW_DOWNLOAD%"     >NUL 2>NUL

REM usercustomize.py
REM ----------------

MD "%CDBTOOLS_PY27%\Python27\site-packages"
echo import dm.cdbtools>"%CDBTOOLS_PY27%\Python27\site-packages\usercustomize.py"

REM init PYTHONUSERBASE
REM -------------------

MD "%CDBTOOLS_PY27%\Scripts"                  >NUL 2>NUL
MD "%CDBTOOLS_PY27%\Python27\site-packages"   >NUL 2>NUL

SET "PYTHONUSERBASE=%CDBTOOLS_PY27%"
echo %PIP_CMD% will install into: %PYTHONUSERBASE%
echo.

PUSHD "%CDBTOOLS_HOME%"
WHERE %PIP_CMD%
%PIP_CMD% install --ignore-installed --user subs\fspath
%PIP_CMD% install --ignore-installed --user pip
POPD

REM ========
:Exit
REM ========
exit
