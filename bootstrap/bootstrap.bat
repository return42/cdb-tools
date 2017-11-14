@REM -*- coding: windows-1252; mode: bat -*-
@ECHO off
REM ----------------------------------------------------------------------------
REM --                             --  File:     cdbtools.bat
REM -- Copyright (C) 2017 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------
REM Purpose:     bootstrap CDBTools
REM ----------------------------------------------------------------------------

SET "PIP_URL=https://pypi.python.org/packages/11/b6/abcb525026a4be042b486df43905d6893fb04f05aac21c32c638e939e447/pip-9.0.1.tar.gz#md5=35f01da3300"
SET "PIP_NAME=pip-9.0.1"

ECHO.
ECHO bootstrap CDBTools package management
ECHO -------------------------------------
ECHO.

FOR %%A IN ("%~dp0\..") DO SET "CDBTOOLS_HOME=%%~fA"
IF %CDBTOOLS_HOME:~-1%==\ SET CDBTOOLS_HOME=%CDBTOOLS_HOME:~0,-1%


REM where python.exe
REM ----------------

ECHO bootstrapping CDBTools requieres Python 2.7.9 ...

IF NOT DEFINED CADDOK_RUNTIME GOTO noCDBRTE
IF NOT EXIST "%CADDOK_RUNTIME%\python.exe" GOTO noCDBRTE
ECHO using CDB's python from: %CADDOK_RUNTIME%\python.exe
SET "MYPYTHON_EXE=%CADDOK_RUNTIME%\python.exe"
GOTO pythonOK

:noCDBRTE
WHERE python.exe >NUL  2>NUL
IF %ERRORLEVEL% EQU 0 GOTO pythonOK
ECHO ERROR: no python.exe available / Python 2.7.9 is needed !!!
exit 42
FOR /f %%i IN ('WHERE python.exe') DO SET "MYPYTHON_EXE=%%i"
ECHO found: %MYPYTHON_EXE%
GOTO pythonOK

:pythonOK
"%MYPYTHON_EXE%" --version
PAUSE

REM source CDBTools environment
REM ----------------------------

call "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat"

REM ATM fspath package is not yet installed; add fspath interim
SET "_MY_OLD_PYTHONPATH=%PYTHONPATH%"
SET "PYTHONPATH=%PYTHONPATH%;%CDBTOOLS_HOME%\subs\fspath"

REM create needed folders
REM ---------------------

MD "%CDBTOOLS_PY27%"            >NUL 2>NUL
MD "%CDBTOOLS_CACHE%"           >NUL 2>NUL
MD "%CDBTOOLS_DIST%"            >NUL 2>NUL
MD "%CDBTOOLS_SW_DOWNLOAD%"     >NUL 2>NUL
MD "%CDBTOOLS_PIP_DOWNLOAD%"    >NUL 2>NUL

REM folders from the user scheme

MD "%CDBTOOLS_PY27%\Scripts"                  >NUL 2>NUL
MD "%CDBTOOLS_PY27%\Python27\site-packages"   >NUL 2>NUL

REM usercustomize.py
REM ----------------

echo import dm.cdbtools>"%CDBTOOLS_PY27%\Python27\site-packages\usercustomize.py"

REM bootstrap pip
REM -------------

del "%CDBTOOLS_CACHE%\%PIP_NAME%.tar.gz" >NUL 2>NUL
rmdir "%CDBTOOLS_CACHE%\%PIP_NAME%" >NUL 2>NUL

IF EXIST "%CDBTOOLS_PIP_DOWNLOAD%\%PIP_NAME%.tar.gz" GOTO downloadPipOK
    "%MYPYTHON_EXE%" -m fspath.main download "%CDBTOOLS_PIP_DOWNLOAD%\%PIP_NAME%.tar.gz" "%PIP_URL%"
:downloadPipOK

"%MYPYTHON_EXE%" -m fspath.main extract  "%CDBTOOLS_PIP_DOWNLOAD%\%PIP_NAME%.tar.gz" "%CDBTOOLS_CACHE%"

PUSHD "%CDBTOOLS_CACHE%\%PIP_NAME%"
"%MYPYTHON_EXE%" setup.py install --user
POPD
CALL "%CDBTOOLS_HOME%\win_bin\cdbtools-fix-launcher.bat"
rmdir "%CDBTOOLS_CACHE%\%PIP_NAME%" >NUL 2>NUL

REM install fspath package, first remove interim from PYTHONPATH
SET "PYTHONPATH=%_MY_OLD_PYTHONPATH%"

PUSHD "%CDBTOOLS_HOME%"
pip install --ignore-installed --user subs\fspath
POPD
CALL "%CDBTOOLS_HOME%\win_bin\cdbtools-fix-launcher.bat"

REM ========
:Exit
REM ========
exit
