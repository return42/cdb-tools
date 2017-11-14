@REM -*- coding: windows-1252; mode: bat -*-
@ECHO off
REM ----------------------------------------------------------------------------
REM --                             --  File:     install-all.bat
REM -- Copyright (C) 2017 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------
REM Purpose:     install CDBTools requirements
REM ----------------------------------------------------------------------------

IF NOT EXIST "%CDBTOOLS_PIP_DOWNLOAD%\*.whl" (
   echo.
   echo ERROR: missing downloads at "%CDBTOOLS_PIP_DOWNLOAD%"
   echo ERROR: please download all first.
   echo.
   pause
   exit 42
)

SET "MY_BUILD_PY=%CDBTOOLS_HOME%\bootstrap\build.py"

ECHO.
ECHO install python requirements
ECHO ----------------------------
ECHO.

python "%MY_BUILD_PY%" install-pypkgs

ECHO.
ECHO install software
ECHO -----------------
ECHO.

python "%MY_BUILD_PY%" install-software

