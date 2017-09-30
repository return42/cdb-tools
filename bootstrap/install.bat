@REM -*- coding: windows-1252; mode: bat -*-
@echo off
REM ----------------------------------------------------------------------------
REM --                             --  File:     cdbtools.bat
REM -- Copyright (C) 2017 darmarIT --  Author:   Markus Heiser
REM --     All rights reserved     --  mail:     markus.heiser@darmarIT.de
REM --                             --  http://www.darmarIT.de
REM ----------------------------------------------------------------------------
REM Purpose:     install CDB-Tool requirements
REM ----------------------------------------------------------------------------

IF NOT DEFINED CADDOK_TOOL (
   echo ERROR: !! This command has to be run in a CDB-shell cdbsh !!
   pause
   GOTO Exit
)

for %%A IN ("%~dp0\..") DO SET "CDBTOOLS_HOME=%%~fA"
IF %CDBTOOLS_HOME:~-1%==\ SET CDBTOOLS_HOME=%CDBTOOLS_HOME:~0,-1%

REM create folder for lokal packages
REM --------------------------------

SET PY27=%CDBTOOLS_HOME%\py27
mkdir %PY27%  > nul  2> nul

REM bootstrap pip
REM -------------

REM This is a small hackisch injection to get *portable* shebangs for the .exe
REM starter installed in /Scripts::
REM
REM   sys.executable='powerscript.exe'
REM
REM In sense of beeing *portable* we need a shebang without absolute pathnames.
REM With above, we get::
REM
REM   #!powerscript.exe
REM

SET PYTHONPATH=%CDBTOOLS_HOME%\bootstrap;%PYTHONPATH%
powerscript -c "import get_pip, sys;sys.executable='powerscript.exe';get_pip.main()" --install-option="--prefix=%PY27%"

REM install requirements
REM --------------------

"%CDBTOOLS_HOME%\winShortcuts\cdbtools" pip-install.bat -r "%CDBTOOLS_HOME%\bootstrap\requirements.txt"

pause
GOTO Exit

REM ----------------------------------------------------------------------------
:Exit
REM ----------------------------------------------------------------------------