@REM -*- coding: windows-1252; mode: bat -*-
@ECHO off
REM ----------------------------------------------------------------------------
REM --                             --  File:     download-all.bat
REM -- Copyright (C) 2017 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------
REM Purpose:     download CDBTools requirements
REM ----------------------------------------------------------------------------

IF NOT DEFINED CDBTOOLS_PIP_DOWNLOAD (
   echo.
   echo ERROR: this command needs a CDBTools environment tu run!
   echo.
   pause
   exit 42
)

SET "MY_BUILD_PY=%CDBTOOLS_HOME%\bootstrap\build.py"

ECHO.
ECHO download python requirements
ECHO ----------------------------
ECHO.

python "%MY_BUILD_PY%" get-pypkgs


ECHO.
ECHO download software
ECHO -----------------
ECHO.

python "%MY_BUILD_PY%" get-software
