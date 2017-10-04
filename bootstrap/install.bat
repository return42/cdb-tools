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

REM bootstrap package management
REM ----------------------------

SET __PYVENV_LAUNCHER__=powerscript.exe
SET PYTHONPATH=%CDBTOOLS_HOME%\bootstrap;%PYTHONPATH%
powerscript -c "import get_pip, sys;sys.executable='powerscript.exe';get_pip.main()" --ignore-installed --install-option="--prefix=%PY27%"

REM CDB-Tools

call %CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat --
PUSHD %CDBTOOLS_HOME%

REM die setuptools in CDB sind steinalt, damit ist ein vernüftiges
REM Package-Management nicht möglich. Die setuptools müssen als
REM erstes installiert werden.
call pip-install setuptools==36.5

REM requirements
REM ------------

call pip-install -r "%CDBTOOLS_HOME%\bootstrap\requirements.txt"

REM .bat wrapper
REM ------------

powerscript -c "import dm.cdbtools; dm.cdbtools.replace_exe_with_bat('%PY27%\Scripts')"

POPD
GOTO Exit

REM ----------------------------------------------------------------------------
:Exit
REM ----------------------------------------------------------------------------
