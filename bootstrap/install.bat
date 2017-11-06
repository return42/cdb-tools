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

SET "PY27=%CDBTOOLS_HOME%\py27"
mkdir "%PY27%"  > nul  2> nul

REM bootstrap package management
REM ----------------------------

REM in absence of an initial virtualenv, we have to set some environments
REM manually

SET "MYPYTHON_EXE=%CADDOK_RUNTIME%\python.exe"
SET "CDBTOOLS_ENV=%CDBTOOLS_HOME%"
SET "CDBTOOLS_PY27=%CDBTOOLS_HOME%\py27"
SET "PATH=%CDBTOOLS_HOME%\win_bin;%CDBTOOLS_PY27%\Scripts;%PATH%"
SET "PYTHONPATH=%CDBTOOLS_HOME%\bootstrap;%CDBTOOLS_HOME%\lib;%CDBTOOLS_PY27%\Lib\site-packages;%PYTHONPATH%"

SET __PYVENV_LAUNCHER__=powerscript.exe
SET PIP_INGNORE_INSTALLED=true

"%MYPYTHON_EXE%" -c "import get_pip, sys;sys.executable='python.exe';get_pip.main()" --ignore-installed --install-option="--prefix=%PY27%"

rem REM die setuptools in CDB sind steinalt, damit ist ein vernüftiges
rem REM Package-Management nicht möglich. Die setuptools müssen als
rem REM erstes nach pip installiert werden.

"%MYPYTHON_EXE%" -c "import pip, sys;sys.executable='python.exe';pip.main()" install --ignore-installed --install-option="--prefix=%PY27%" setuptools==36.6

"%MYPYTHON_EXE%" -c "import pip, sys;sys.executable='python.exe';pip.main()" install --ignore-installed --install-option="--prefix=%PY27%" virtualenv

REM "%MYPYTHON_EXE%" -c "import pip, sys;sys.executable='python.exe';pip.main()" install --ignore-installed --install-option="--prefix=%PY27%" -e "%CDBTOOLS_HOME%\subs\fspath"

"%MYPYTHON_EXE%" -c "import dm.cdbtools.bootstrap;dm.cdbtools.bootstrap.replace_exe_with_bat('%CDBTOOLS_PY27%\Scripts')" 2> NUL


echo create virtualenv "%CDBTOOLS_PY27%"
call virtualenv "%CDBTOOLS_PY27%"

call "%CDBTOOLS_HOME%\win_bin\cdbtools-activate.bat"

"%MYPYTHON_EXE%" -c "import dm.cdbtools.bootstrap;dm.cdbtools.bootstrap.replace_exe_with_bat('%CDBTOOLS_PY27%\Scripts')" 2> NUL


rem REM requirements of CDB-Tools
rem REM -------------------------

PUSHD "%CDBTOOLS_HOME%"
call "%CDBTOOLS_HOME%\win_bin\pip-install.bat" -r "%CDBTOOLS_HOME%\bootstrap\requirements.txt"
POPD
